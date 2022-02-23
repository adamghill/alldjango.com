---
template: base.html
title: Unique, but obfuscated URLs in Django
description: How to create unique, but obfuscated URLs in Django.
---

When building a website, sometimes you want a URL for a specific piece of data, but there isn't a clear field that should be [`slugified`]({% url 'content' 'tips/url-slugs' %}). This usually happens when the name or title of the data might get updated in the future which would change the URL `slug`. But, "[cool URLs never change](https://www.w3.org/Provider/Style/URI)"!

Let's pretend that you are building an e-commerce system. You want to have a detail page for each product. However, just using a `slug` based on the product name would mean the URL might change if the product's name ever got updated.

```python
from django.db import models

class Product(models.Model):
    id = models.BigAutoField()  # making the `id` explicit
    name = models.CharField(max_length=255)
```

The easiest approach in this situation would be to use the database's auto-generated primary key for the URL. By default in Django, the primary key is a [`BigAutoField`](https://docs.djangoproject.com/en/stable/ref/models/fields/#bigautofield) which basically means it starts at 1 for the first product and increments up for each new piece of data to a very, very large number (e.g. 9223372036854775807) So, unless you are `Instagram` you are probably going to be fine.

**WARNING**

However, using an integer in the URL exposes private information about your data that you probably want to keep private. It also allows malicious users to easily increment the id to find all the products in your system.

```
Alice sees that a product is located at /products/123.

Alice then proceeds to look at the next product at /products/124.

Alice has now hacked the mainframe.
```

## Obfuscated identifiers

There are a few options to create unique identifiers, but also stay away from exposing the auto-incrementing integers in your database.

### `UUID`

One approach to create URLs that are obfuscated, but also guaranteed to be unique is use `uuid.uuid4` and the [`UUIDField`](https://docs.djangoproject.com/en/stable/ref/models/fields/#uuidfield) provided by Django.

```python
import uuid
from django.db import models

class Product(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
```

Using a `UUID` as the primary key is supported by Django, but I tend to use a separate field in addition to the implicit `id` that Django will use by default. Why? Honestly, it is mostly out of force of habit (and the, maybe?, irrational fear that a `UUID` will be slower than using an integer in `PostgreSQL` -- more details in [this StackOverflow question](https://stackoverflow.com/questions/34230208/uuid-primary-key-in-postgres-what-insert-performance-impact)). But, you can see an example of using `UUID` as the primary key in the [Django docs](https://docs.djangoproject.com/en/stable/ref/models/fields/#uuidfield) if you want to try it out.

Whether it's the actual primary key or not, the `urlconf` can then look up an object by using the built-in `uuid` [path converter](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters).

The first part, `uuid`, is the `path converter`. The second part is the argument passed into the view arguments.

```python
# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('products/<uuid:identifier>/', views.products),
]
```

```python
# views.py
from django.shortcuts import render
from product.models import Product

def products(request, identifier):
    product = Product.objects.get(identifier=identifier)
    return render(request, "product.html", context={"product": product})
```

The upside of `UUID`s are that they are basically mathmatically guaranteed to be unique and Django supports them without any additional libraries. The downside is that they make URLs ugly. :shruggie:

### `nanoid`

[nanoid](https://github.com/ai/nanoid) is an attempt to have the same quaranteed uniqueness that you get with `UUID`, but in a more URL-friendly identifier. The [Python port](https://github.com/puyuan/py-nanoid) looks like a good approach if you are worried about URL collisions.

### `shortuuid`

A second approach is to use [shortuuid](https://github.com/skorokithakis/shortuuid) which I have used in a lot of projects in the past. Especially useful is the ability to pass in a string as a namespace. `shortuuid` includes a [Django model field](https://github.com/skorokithakis/shortuuid#django-field) for ease of use.

```python
from django.db import models
from shortuuid.django_fields import ShortUUIDField

class Product(models.Model):
    identifier = ShortUUIDField(length=8)  # the default length is 22 characters
```

### `RandomCharField`

A third approach I've been using recently is to use the `RandomCharField` included in the [django-extensions](https://django-extensions.readthedocs.io/en/latest/field_extensions.html) package with a `unique` constraint on the database field. With a length of 8, there are 3.4 million possible combinations which is probably good enough (until it isn't).

```python
from django.db import models
from django_extensions.db.fields import RandomCharField

class Product(models.Model):
    identifier = RandomCharField(length=8, editable=False, unique=True)
```

## What I do 🌟

Hopefully that gave you some ideas of how to approach creating detail pages for the future. Personally, I tend to:

- use the default `id` in the model of `BigAutoField`
- add a `slug` field if it would be useful for SEO purposes
- use `RandomCharField` with a `unique` constraint on the model which gives me clean enough URLs and they are unique enough for my purposes
