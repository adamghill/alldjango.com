---
template: base.html
title: Prettier URLs with automatic slug generation 🐌
description: How to create cleaner URLs with slugs in Django.
---

When building a website, sometimes you want a URL for a specific piece of data, but the URL should be nicer than `/products/123`. A `slug` can be used for a prettier URL like `/products/really-cool-headphones` and, bonus points!, it's better for SEO as well.

## `SlugField`

Django has a built-in [`SlugField`](https://docs.djangoproject.com/en/stable/ref/models/fields/#slugfield) designed for this. It seems like the right approach, but you have to manually update the `slug` unless you always use the built-in admin (in which case you can use [`prepopulated_fields`](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.prepopulated_fields)).

If you want the `slug` generation to even more automated you will need an external library. Luckily there are two great ones to choose from.

## `django-extensions`

The "kitchen sink" package that is [`django-extensions`](https://django-extensions.readthedocs.io/) has [`AutoSlugField`](https://django-extensions.readthedocs.io/en/latest/field_extensions.html#current-database-model-field-extensions). The `populate_from` kwarg for `AutoSlugField` takes in a list of fields or model methods to generate a `slug`.

```python
from django.db import models
from django_extensions.db.fields import AutoSlugField

class Article(models.Model):
    title = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from=["title", "author_name","get_publish_date"])

    def get_publish_date(self):
        ...
```

You can also use a custom method to create the `slug` with the `slugify_function` kwarg.

## `django-autoslug`

[`django-autoslug`](https://django-autoslug.readthedocs.io/) is a tiny focused package just for automatically generating `slugs`.

```python
from django.db import models
from autoslug import AutoSlugField

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="title")
```

It also has some more specialized features which make sure that your `slugs` are unique across the entire table of data. There are custom methods to create the slug as well.

## Have your cake and eat it, too? 🎂

Another approach that sites like StackOverflow use is to have an identifier and the slug in the URL. Look at an example URL closely:

```shell
https://stackoverflow.com/questions/34230208/uuid-primary-key-in-postgres-what-insert-performance-impact
```

The slug at the end isn't used to look up the question at all. You can verify this if you don't believe me by changing the slug and going to the URL again.

`/questions/324230208` is the question identifier and is the only part that is used to look up the specific question. Once the question has been found if the `uuid-primary-key-in-postgres-what-insert-performance-impact` portion of the URL is different than the question's `slug` in the database, they redirect to a URL with the correct `slug`. This ensures that if the slug ever changes users will always get to the right URL.

This is one way to have nicer looking URLs, but handle if the `slug` might change.

## Keep a history of all `slugs` forever

Another approach is to keep a list of `slugs` that are generated as a foreign key (i.e. one-to-many). Inside your view, you would include that table in your query, but redirect to the latest slug if necessary.

```python
def product(request, slug):
    product = Product.objects.get(slugs__slug=slug)

    last_created_slug = product.slugs.all().order_by("-created").first()

    if last_created_slug.slug != slug:
        return redirect("product", slug=last_created_slug.slug)

    ...
```

Personally, this approach seems like overkill and not worth the hassle.

## My recommendation 🌟

Both of the additional libraries are great. Personally, I tend to:

- use `AutoSlugField` from `django-extensions` if I have already included it in the project and the slugs I need to create are straight-forward
- only include `django-autoslug` if I need the additional functionality it provides
