---
template: base.html
---

## No fluff help for perfectionists with deadlines

> Deliver business value quickly without sacrificing your sanity by sticking to [boring technologies](http://boringtechnology.club/) and skipping the fads.

<br />

### ⚡ Optimize for developer speed and maintainability

- Skip the tangled web of microservices and use a Django monolith
- Handle data with PostgreSQL and cache with Redis
- Offload slow processing to [`RQ`](https://github.com/rq/django-rq) or [`django-db-queue`](https://github.com/dabapps/django-db-queue)
- Use Django templates and the least amount of JavaScript possible while still providing a great user experience

<br />

### [Articles](/articles)

{% directory_contents "articles" as articles %}

{% for article in articles %}
{% if not article.draft %}
✨ [{{ article.title }}]({{ article.slug }})<br/>
{% endif %}
{% endfor %}

### [Tips](/tips)

{% directory_contents "tips" as tips %}

{% for tip in tips %}
{% if not tip.draft %}
✨ [{{ tip.title }}]({{ tip.slug }})<br/>
{% endif %}
{% endfor %}
