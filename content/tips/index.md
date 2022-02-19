---
template: base.html
title: Tips
---

{% directory_contents as directory_contents %}

{% for content in directory_contents %}
{% if not content.draft %}

- [{{ content.title }}]({{ content.slug }})

{% endif %}
{% endfor %}
