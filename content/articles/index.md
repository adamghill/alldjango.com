---
template: base.html
title: Articles
---

{% directory_contents as articles %}

{% for article in articles %}
✨ [{{ article.title }}]({{ article.slug }})<br />
{% endfor %}
