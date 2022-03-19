---
template: base.html
title: Optimize the Django ORM 🚀
date: 2018-12-01 22:33:16 -0400
categories: django python
description: How to optimize Django ORM queries to improve site performance.
---

Recently, I have been optimizing some functions that were slower than expected. As with most MVPs, the initial iteration was to get *something* working and out there. Looking at [Scout APM](https://scoutapp.com/) revealed that some of the database queries were slow, including several `n+1` queries. The `n+1` queries happened because I was looping over a set of models, and either updated or selected the same thing for each model. My goal was to reduce any duplicate queries, and squeeze out as much performance as I could by refactoring the naive, straight-forward operations into more performant equivalents.

In all honesty, the code is slightly more complicated to read through now, but I cut the time for my use-case in half without changing anything else about the server or database.

## Use the ORM, Luke

One of Django's main benefits is the built-in models and object-relational mapper (ORM). It provides a quick to use, common interface for data operations for your models and can handle most queries pretty easily. It can also do some tricky SQL once you understand the syntax.

It's easy to get building quickly. It’s also easy to end up making more (costly) SQL calls than you realize.

## Hasta la vista, models

Here are some sample models that will be used to illustrate some of the concepts below.

```python
# models.py
class Author(models.Model):
    name = models.CharField(max_length=50)

class Book(models.Model):
    author = models.ForeignKey(Author, related_name="books", on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
```

## Show me the sql (part 1)

Because the SQL calls *are* abstracted behind a simple API, it's easy to end up making more SQL calls than you realize. You can retrieve a close approximation with the `query` attribute on a QuerySet, but heed the warning about it being an "[opaque representation](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet)".

```python
books = Book.objects.all()
print("books.query", books.query)
```

## Show me the sql (part 2)

You can also add `django.db.logging` to your configured loggers to see generated SQL get printed out to the console.

```python
"loggers": {
    "django.db.backends": {
        "level": "DEBUG",
        "handlers': ["console", ],
    }
}
```

## Show me the sql (part 3)

You can also print out the time and generated SQL that Django stores on the database connection.

```python
from django.db import connection

books = Book.objects.all()
print("connection.queries", connection.queries)
```

## The one Toolbar to rule them all

If your code is called from a view, the easiest way to start deciphering what SQL is generated is installing [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/). DDT provides an unbelievably helpful diagnostic tool which shows all of the SQL queries being run, how many are similar to each other and how many are duplicated. You can also look at the query plan for each SQL query and dig into why it might be slow.

## Select and prefetch *all* the relateds

One thing to realize is that Django's ORM is pretty lazy by default. It will not run queries until the result has been asked for (either in code or directly in a view). It also won't join models by their ForeignKeys until needed. Those are beneficial optimizations, however they can bite you if you don't realize.

```python
# views.py
def index(request):
    books = Book.objects.all()

    return render(request, { "books": books })
```

{% verbatim %}

```html
<!-- index.html -->
{% for book in books %} Book Author: {{ book.author.name }}
<br />
{% endfor %}
```

{% endverbatim %}

In the code above, each book in the `for loop` in `index.html` will call the database again for the author's name. So, there would be 1 database call to retrieve the set of all books, and then an additional database call for every book in the list.

The way to prevent the extra database calls is to use [`select_related`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#select-related) to force Django to join to the other model once and prevent subsequent calls if that relation is used.

Updating the view code to use a `select_related` would reduce the total sql calls to only 1 for the same Django template.

```python
# views.py
def index(request):
    books = Book.objects.select_related("author").all()

    return render(request, { "books": books })
```

In some cases `select_related` won't work, but `prefetch_related` will. The Django documentation has [lots more details](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#prefetch-related) about when to use `prefetch_related`.

## Beware the instantiating of models

When the Django ORM creates a `QuerySet` it takes the data retrieved from the database and populates the models. However, if you don't need a model, there are a few ways to skip constructing them unnecessarily.

[`values_list`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#values-list) will return a list of tuples for all of the columns specified. Particularly useful is the `flat=True` keyword argument which returns a flattened list if only one field is specified.

```python
# get a list of book ids to use later
book_ids = Book.objects.all().values_list("id", flat=True)
```

You can also create a dictionary with the pair of data that might be required later with [`values`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet.values). For example, if I was going to need blog ids and their urls:

```python
# get a dictionary of book id->title
book_ids_to_titles = {b.get("id"): b.get("title") for b in Book.objects.all().values("id", "title")}
```

To get all of the book ids: `book_ids_to_titles.keys()`. To get all titles: `book_ids_to_titles.values()`.

Somewhat related, [`bidict`](https://bidict.readthedocs.io/en/master/) is fantastic for an easy way to retrieve a dictionary's key from its value and vice versa (as opposed to keeping around 2 dictionaries).

```python
book_ids_to_titles = bidict({
    "1": "The Sandman",
    "2": "Good Omens",
    "3": "Coraline",
})

assert book_ids_to_titles["1"] == book_ids_to_titles.inv["The Sandman"]
```

## Filtering on ids makes the world go 'round

Using `filter` translates to a `WHERE` clause in SQL, and searching for an integer will [almost always be faster than searching on a string](https://stackoverflow.com/questions/2346920/sql-select-speed-int-vs-varchar) in Postgres. So, `Book.objects.filter(id__in=book_ids)` will be slightly more performant than `Book.objects.filter(title__in=book_titles)`.

## Only and defer to your heart's content

[`Only`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet.only) and [`Defer`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet.defer) are mirror opposite methods to acheive the same goal of only retrieving particular fields for your model. [`Only`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet.only) works by SELECTing the specified database fields, but not filling in any non-specified fields. [`Defer`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet.defer) works the opposite way, so the fields will not be included in the SELECT statement.

However, this note in the Django documentation is telling:

> They provide an optimization for when you have analyzed your queries closely and understand _exactly_ what information you need and have measured that the difference between returning the fields you need and the full set of fields for the model will be significant.

## Annotate and carry on

For some code, I was getting a count for each model in a list in a loop.

```python
for author in Author.objects.all():
    book_count = author.books.count()
    print(f"{book_count} books by {author.name}")
```

This will create one SQL `SELECT` statement for every author. Instead, using an [`annotation`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet.annotate) will create one SQL query.

```python
author_counts = (
    Author.objects
    .annotate(book_count=Count("book__id"))
    .values("author__name", "book_count")
)

for obj in author_counts:
    print(f"{obj.get('book_count')} books by {obj.get('author__name')}")
```

[`Aggregation`](https://docs.djangoproject.com/en/2.1/topics/db/aggregation/) is the simpler version of [`annotation`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet.annotate) if you want calculate a value for all objects in a list (e.g. get the maximum id from a list of models). [`Annotation`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#django.db.models.query.QuerySet.annotate) is useful if you want to calculate values over each model in a list and get the output.

## Bulk *smash*! Errr, create

Creating multiple objects with one query is possible with [`bulk_create`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#bulk-create). There are some caveats to using it, and unfortunately you don't get a list of ids created after the insert which would be useful. But, for simple use-cases it works great.

```python
author = Author(name="Neil Gaiman")
author.save()

Book.objects.bulk_create([
    Book(title="Neverwhere", author=author),
    Book(title="The Graveyard Book", author=author),
    Book(title="The Ocean at the End of Lane", author=author),
])
```

## We want to bulk *you* up

[`update`](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#update) is a method on `QuerySet`, so you are able to retrieve a set of objects and update a field on all of them with one SQL query. However, if you want to update a set of models with different field values [`django-bulk-update`](https://github.com/aykut/django-bulk-update) will come in handy. It automagically creates one SQL statement for a set of model updates even if they have differing values.

```python
from django.utils import timezone
from django_bulk_update.helper import bulk_update

books = Book.objects.all()
for book in books:
    book.title = f"{book.title} - {timezone.now}"

# generates 1 sql query to update all books
bulk_update(books, update_fields=['title'])
```

## Gonna make you sweat (everybody Raw Sql now)

If you really can't figure out a way to get the Django ORM to generate performant SQL, [`raw sql`](https://docs.djangoproject.com/en/2.1/ref/models/expressions/#django.db.models.expressions.RawSQL) is always available, although it's not generally advised to use it unless you have to.

## Automatic for the people

[django-auto-prefetch](https://github.com/tolomea/django-auto-prefetch) will automatically prefetch the foreign keys or one-to-one models. It's a great way to create more performant queries just by inheriting from a different base `Model` class. Highly recommended to save yourself from manually trying to figure out what fields are needed in `select_related` or `prefetch_related` method calls.

## Putting on the ritz

The Django documentation is generally really helpful and will give you more in-depth details about each technique above. If you know of any other approaches to squeezing the most performance out of Django, I would love to hear about them at [twitter.com/adamghill](https://twitter.com/adamghill).
