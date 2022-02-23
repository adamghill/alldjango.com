---
template: base.html
title: Articles
description: A list of all articles.
---

{% directory_contents as articles %}

{% for article in articles %}
{% if not article.draft %}
✨ [{{ article.title }}]({{ article.slug }})<br />
{% endif %}
{% endfor %}
