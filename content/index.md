---
template: base.html
---

<h1 style="text-align: center; margin-bottom: 40px;">No bullshit help for<br />perfectionists with deadlines</h1>

> Deliver business value quickly without sacrificing your sanity by sticking to [boring technologies](http://boringtechnology.club/) and skipping the fads.

<br />

### ⚡ Optimize for developer speed and maintainability

- Skip the tangled web of microservices and use Django apps to stay in a delightful monolith
- Stick to tried-and-true technology like `PostgreSQL` and `Redis`
- Use server-side templates and the least amount of JavaScript possible while still providing a great user experience
- Offload slow processing to a background queue like [`django-q2`](https://github.com/django-q2/django-q2) to keep rendering time fast

<br />

### [Articles](/articles)

{% directory_contents "articles" order_by="-date" as articles %}

{% for article in articles %}
{% if not article.draft %}
✨ [{{ article.title }}]({{ article.slug }})<br/>
{% endif %}
{% endfor %}

### [Tips](/tips)

{% directory_contents "tips" order_by="-date" as tips %}

{% for tip in tips %}
{% if not tip.draft %}
✨ [{{ tip.title }}]({{ tip.slug }})<br/>
{% endif %}
{% endfor %}
