---
template: base.html
---

# alldjango

## No fluff help for perfectionists with deadlines

Deliver business value quickly without sacrificing your sanity.

### Optimize for developer speed and maintainability

- Skip the tangled web of microservices and be content with a monolith
- Handle data with PostgreSQL and Redis
- Offload slow processing to [`RQ`](https://github.com/rq/django-rq) or [`django-db-queue`](https://github.com/dabapps/django-db-queue)
- Use the least amount of JavaScript possible, but still provide a great UX
- Stick to [boring technologies](http://boringtechnology.club/) and skip the fads

### Articles

{% directory_contents "articles" as directory_contents %}

{% for content in directory_contents %}

- [{{ content.title }}]({{ content.slug }})

{% endfor %}

### Tips

{% directory_contents "tips" as directory_contents %}

{% for content in directory_contents %}

- [{{ content.title }}]({{ content.slug }})

{% endfor %}
