---
template: base.html
title: Easily update URL querystrings in a template
description: How to dynamically update URLs with a template tag.
tags: django,templatetag
---

On [devmarks.io](https://devmarks.io) I have a side bar with tags that, when clicked, filter the current list of bookmarks. I use querystrings for those filters so I needed a way to dynamically make links add a querystring to the current url.

The following example is how the template tag works in a template.

```html
{% load url_tags %}

<!-- assume a current path of https://devmarks.io/bookmarks?filter=filter-0 -->

<a href="{% add_query_string replace=True filter='filter-1' %}">Replaces the `filter` querystring with `filter=filter-1` on the current URL</a>
<!-- href would be https://devmarks.io/bookmarks?filter=filter-1 -->

<a href="{% add_query_string filter='filter-2' %}">Adds a new `filter=filter-2` querystring on the current URL</a>
<!-- href would be https://devmarks.io/bookmarks?filter=filter-0&filter=filter-1 -->

<a href="{% add_query_string view='view-0' %}">Adds a new `view=view-0` querystring on the current URL</a>
<!-- href would be https://devmarks.io/bookmarks?filter=filter-0&view=view-0 -->
```

And here is the Django template tag that provides the functionality above.

```python
# templatetags/url_tags.py

import urllib.parse as urlparse
from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def add_query_string(context, url: str = None, replace=False, **params) -> str:
    """
    Mutates a querystring.
    
    Args:
        url: If no `url` is passed in, the current request context is used by default.
        replace: Replace all keys of the querystring if `True`. Defaults to `False`.
    """

    if not url:
        request = context.get("request")
        url = request.get_full_path()

    # Tweaked from https://stackoverflow.com/a/2506477
    url_parts = list(urlparse.urlparse(url))
    query = None

    if replace:
        query = urlparse.parse_qsl(url_parts[4])
        new_query = []
        keys = set()

        for (k, v) in query:
            keys.add(k)

            if k in params:
                new_query.append((k, params[k]))
            else:
                new_query.append((k, v))

        query = new_query

        # Handle params that aren't currently in the querystring
        for (k, v) in params.items():
            if k not in keys:
                query.append((k, v))
    else:
        query = urlparse.parse_qsl(url_parts[4])

        for k, v in params.items():
            query.append((k, v))

    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)
```

This template tag provides a way to dynamically tweak a URL's querystring easily. Hopefully it works as well for you as it does for me.
