---
template: base.html
title: Django Reversion + Wagtail = magic 🧙
date: 2019-09-18 21:24:16 -0500
categories: django python wagtail
description: How to use Django Reversion and Wagtail together to audit changes.
---

Track versions of Wagtail _snippets_ for an automatic audit trail to find the bad guys.

## There are trade-offs with everything (or how I stopped worrying and learned to love Wagtail CMS)

[Wagtail](https://wagtail.io/) is a CMS framework built on top of Django that takes away some of tedium of creating a CMS from scratch. It has a nice extendable interface for editors to interact with, page reversion tracking, a spiffy admin UI, easy uploading of images, and [lots of other goodies](https://wagtail.io/features/).

I'll be honest -- coming from Django where I have a pretty good grasp of how things work (and where to figure things out if I need to) was a hard transition to Wagtail. It definitely took a little time to understand its philosophy around content.

But, at this point, I have come to appreciate all of the benefits that Wagtail provides... and work around some of the pieces that I like less. One thing that took me a while to understand is that Wagtail uses the term _snippet_ to refer to Django models that aren't explicitly a _Page_. Coming from Django, I am used to defining a data model and tying models together with many-to-many or foreign key relationships. _Snippets_ are where to store those pieces of information that could be shared with many different _Page_ models. However, _snippets_ feel like they are not completely integrated into the Wagtail experience, and they lose a lot of the nice functionality that comes "for free" with a page model -- one glaring omission is the lack of revisions for _snippets_. There are a few open issues for this in Wagtail (notably https://github.com/wagtail/wagtail/issues/4541 and https://github.com/wagtail/wagtail/issues/2270).

## Django audits in one easy payment of $0

One package that I have really appreciated in the past with a normal Django application is [django-reversion](https://django-reversion.readthedocs.io/) which integrates tightly into the Django admin and automatically saves versions of an object as an audit trail. Wagtail provides something very similar for _Page_ models, but snippets eren't invited to the party and feel very left out.

## ¡Ay, caramba! Automatic auditing for Wagtail snippets!

All is well in Wagtail-land, though! With a little perserverance, Wagtail _snippets_ can also get automatic revisions and it isn't **too** hard.

### Setup django-reversion

First, install `django-reversion` with the normal installation steps. Unfortunately, Wagtail won't tie into the same automatic magic that `django-reversion` uses for the Django admin, but it has a stellar API you can call explicitly.

### Register snippet models with django-reversion

For _snippet_ models, you will need to add the `@reversion.register()` decorator above the `@register_snippet` in `models.py`.

```python
from django.db import models
import reversion
from wagtail.core.models import ClusterableModel, Orderable
from wagtail.snippets.models import register_snippet


@reversion.register()
@register_snippet
class Book(Orderable, ClusterableModel):
    title = models.CharField(max_length=255)
```

### Override the Wagtail views

Next, you will need to override the Wagtail views for the snippets you want to audit in `wagtail_hooks.py`.

```python
from reversion.revisions import add_to_revision, create_revision, set_comment, set_user
from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.views import CreateView, EditView

from .models import Book


class RevisionEditView(EditView):
    def form_valid(self, form, *args, **kwargs):
        form_valid_return = super().form_valid(form, *args, **kwargs)

        with create_revision():
            set_comment(self.get_success_message(self.instance))
            add_to_revision(self.instance)
            set_user(self.request.user)

        return form_valid_return


class RevisionCreateView(CreateView):
    def form_valid(self, form, *args, **kwargs):
        form_valid_return = super().form_valid(form, *args, **kwargs)

        ## Call form.save() explicitly to get access to the instance
        instance = form.save()

        with create_revision():
            set_comment(self.get_success_message(instance))
            add_to_revision(instance)
            set_user(self.request.user)

        return form_valid_return


class BookAdmin(ModelAdmin):
    model = Book
    edit_view_class = RevisionEditView
    create_view_class = RevisionCreateView
```

## Happy trails

Overriding the ModelAdmin classes by setting the `edit_view_class` and `create_view_class` settings and `django-revision` is the real magic here. But, be sure to note the weirdness in the `CreateView` to get an `instance` that is usable. In testing it doesn't create multiple instances of the model, however, I would not be surprised if there are duplicate database calls because of the implementation.

> ##### Tested with the following package versions
>
> - Python 3.7.4
> - [Django](https://www.djangoproject.com/)==2.2.4
> - [wagtail](https://wagtail.io/)==2.6.1
> - [django-reversion](https://django-reversion.readthedocs.io/)==3.0.4
