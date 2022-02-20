---
template: base.html
title: Searching within an area with GeoDjango and PostGIS 🌎
date: 2016-06-14 22:33:16 -0400
categories: django python geodjango postgresql postgis
---

One feature of [InHerSight.com](https://www.inhersight.com) that has been proved to be extremely useful is the ability to use location as a filter when [exploring potential companies](https://www.inhersight.com/discover). Luckily, we are using [Django](https://www.djangoproject.com/) and [PostgreSQL](https://www.postgresql.org) which has robust support for geographic querying using [GeoDjango](https://docs.djangoproject.com/en/1.9/ref/contrib/gis/) and [PostGIS](http://postgis.net/). I also utilize the awesome [django-cities](https://github.com/coderholic/django-cities) package for an astounding amount of data related to places.

There wasn't a lot of great documentation on StackOverflow or through my searching, so I did a lot of trial and error to get to a sufficiently performing solution.

A simplified version of the initial code looked something like this:

```python
# models.py
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db.models import PointField
from cities.models import City

class Company(models.Model):
    name = models.CharField()
    places = GenericRelation(Place)

class Place(models.Model):
    point = PointField()
    city = models.ForeignKey(City)


# views.py
from django.db.models import F
from django.contrib.gis.db.models import PointField
from cities.models import City

distance_miles_to_search = 50
point = PointField()  # get a point of a particular place (usually by latitude/longitude)
companies = Company.objects.filter(places__point__distance_lte=(point, D(mi=distance_miles_to_search))).annotate(closest_city_id=F('places__city'))
```

The `distance_lte` filter definitely worked for the initial MVP, however, as we continued to add in companies and locations, we started noticing some blocking when searching for companies by location. Then, when we would get a burst of traffic the slowdowns became even more evident. New Relic and Heroku's metrics panels were very helpful pinpointing where the slowdowns were happening. However, even after many rounds of optimizations, InHerSight hit a brickwall trying to squeeze any more performance from the existing architecture.

I thought I could reduce the blocking by setting up a readonly replica for the master database by distributing the reads across two databases. That definitely helped, but even with minimal load distance-based queries were still around 2500ms -- well above the threshold for acceptability.

The `distance_lte` filter translates to the [ST_Distance](http://postgis.net/docs/ST_Distance.html) function in PostGIS. I had read in various places (specifically, [http://stackoverflow.com/questions/7845133/how-can-i-query-all-my-data-within-a-distance-of-5-meters](http://stackoverflow.com/questions/7845133/how-can-i-query-all-my-data-within-a-distance-of-5-meters) and [http://stackoverflow.com/questions/2235043/geodjango-difference-between-dwithin-and-distance-lt](http://stackoverflow.com/questions/2235043/geodjango-difference-between-dwithin-and-distance-lt)) that there was also the `dwithin` filter clause in GeoDjango, but I never could get it working correctly until digging into [http://stackoverflow.com/questions/31940674/optimal-query-in-geodjango-postgis-for-locations-within-a-distance-in-meters](http://stackoverflow.com/questions/31940674/optimal-query-in-geodjango-postgis-for-locations-within-a-distance-in-meters). `dwithin` translates to the [ST_DWithin](http://postgis.net/docs/ST_DWithin.html) function in PostGIS and uses a spatial index that [should result in faster performance](http://stackoverflow.com/questions/7845133/how-can-i-query-all-my-data-within-a-distance-of-5-meters#comment9588147_7845663).

The simplified version of my code to use the `dwithin` filter clause:

```python
# views.py
from django.contrib.gis.measure import D
from django.db.models import F
from cities.models import City


def convert_miles_to_degrees(miles):
    '''
    Convert miles to degrees. Somewhat imprecise, but probably good enough.
    '''

    meters = D(mi=miles).m
    degrees = (meters / 40000000 * 360)

    return degrees

degrees = convert_miles_to_degrees(50)
point = City.objects.get(pk=...).location
companies = Company.objects.filter(places__point__dwithin=(point, degrees))\
                .annotate(closest_city_id=F('places__city'))
```

Using the `ST_DWithin` improved location queries by approximently 30x on my local development machine and a still very respectable 10x on the live databases. That query now hovers around 200ms even with load. I'm caching data pretty aggressively when I can and there might be some opportunities to pre-compute some typical searches or use something like ElasticSearch or Lucene in the future, but just switching from `ST_Distance` to `ST_DWithin` significantly improved location-based query performance.
