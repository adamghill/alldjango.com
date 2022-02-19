---
template: base.html
title: Django inclusion tags can modify page context
date: 2020-03-26 21:24:16 -0500
categories: django python
---

Django [inclusion tags](https://docs.djangoproject.com/en/stable/howto/custom-template-tags/#inclusion-tags) are super useful, but they have a fun quirk that could create some havoc.

# The setup

Creating custom template tags in Django takes a little to get used to, but a coworker recently stumbled on a weird bug and it took me by surprise. It was related to a custom inclusion tag and the `takes_context` parameter.

An example inclusion tag yanked from the Django documentation:

```python
@register.inclusion_tag('link.html', takes_context=True)
def jump_link(context):
    return {
        'link': context['home_link'],
        'title': context['home_title'],
    }
```

However, instead of returning a dictionary from the function, my coworker had modified the context and returned it directly:

```python
@register.inclusion_tag('link.html', takes_context=True)
def jump_link(context):
    context['link'] = context['home_link']
    context['title'] = context['home_title']
    return context
```

Maybe unsurprisingly, the template tag worked just fine, however it had unintended ramifications if the variables being returned conflicted with a key already defined in the page context. So, if the view code contained `link` in the page context, then the second example of `jump_link` would override the that template variable from that point on -- making the value of the view context dependent on where the inclusion tag is placed in the template.

The following Django template should hopefully make clear what could potentially happen:

{% verbatim %}

```html
Initial view context variable: {{ "{{ link " }}}}<br />
{{ "{% jump_link " }}%}<br />
Clobbered view context variable from the inclusion tag: {{ "{{ link " }}}}<br />
```

{% endverbatim %}

This _makes sense_ once I realized that modifying the context while the template is rendering is going to affect rendering later portions of the template, however I definitely did not expect it to happen. In general, I would recommend against changing the context inside of the template tag because it makes debugging what happens in the template much more difficult.
