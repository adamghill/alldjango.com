---
template: base.html
title: Articles
---

{% directory_contents as directory_contents %}

{% for content in directory_contents %}

- [{{ content.title }}]({{ content.slug }})

{% endfor %}