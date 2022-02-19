---
template: base.html
title: URL Slugs
---

When building a website, sometimes you want a URL for a specific piece of data, but you want the URL to be nicer than `/products/123`. A `slug` can be used to generate a prettier URL like `/products/really-cool-headphones` and, bonus points!, it's better for SEO as well.

## `SlugField`

Django has a built-in [`SlugField`](https://docs.djangoproject.com/en/stable/ref/models/fields/#slugfield) designed for slugs. It's useful, but the only way to pre-populate it with [`prepopulated_fields`](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.prepopulated_fields) in the Django admin.

If you want something a little more automatic check out the next few libraries.

## `django-autoslug`

[`django-autoslug`](https://django-autoslug.readthedocs.io/) provides the ability for a field to automatically by slugified when the field is created which is very useful.

```python
from django.db import models
from autoslug import AutoSlugField

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="title")
```

There are a ton of other options to make sure the slug is unique and custom methods to create the slug.

## `django-extensions`

The kitchen sink that is [`django-extensions`](https://django-extensions.readthedocs.io/) has [`AutoSlugField`](https://django-extensions.readthedocs.io/en/latest/field_extensions.html#current-database-model-field-extensions). The `populate_from` kwarg takes in a list of fields or model methods to generate a slug.

```python
from django.db import models
from django_extensions.db.fields import AutoSlugField

class Article(models.Model):
    title = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from=["title", "author_name", "get_publish_date"])

    def get_publish_date(self):
        ...
```

You can also have a custom method that gets called to create the slug with the `slugify_function` kwarg.

## Have your cake and eat it, too?

Another approach that sites like StackOverflow use is to try to have their cake and eat it, too. Look at an example URL closely and you will see a unique identifier AND a slug: https://stackoverflow.com/questions/34230208/uuid-primary-key-in-postgres-what-insert-performance-impact. The slug at the end isn't used to look up the question at all. The integer is the identifier and if the question that is looked up has a different slug than the last part of the URL, they redirect the url so the slug is correct. It is one way to have nicer looking URLs, but also a canonical identifier. The same approach would work if you don't want the integer identifier exposed.

## What I do

Both of the additional libraries are great. Personally, I tend to:

- use `AutoSlugField` from `django-extensions` if I have already included it in the project and the slugs I need to create are straight-forward
- include `django-autoslug` if I need additional functionality
