---
template: base.html
title: Articles
---

{% directory_contents as articles %}

{% for article in articles %}
{% if not article.draft %}
✨ [{{ article.title }}]({{ article.slug }})<br />
{% endif %}
{% endfor %}
