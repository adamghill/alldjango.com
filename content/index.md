---
template: base.html
---

# alldjango

## No fluff help for perfectionists with deadlines

Deliver business value quickly without sacrificing your sanity. Follow tried and true tips for success and not just the latest hyped tech fad.

## How?

- Optimize for developer speed and maintainability
- Python and Django is fast enough
- A monolith is better than a tangled web of microservices
- PostgreSQL, Redis, and RQ can handle any type of data
- Most functionality is best in Python, with small bits of JavaScript only when needed

## Articles

{% directory_contents "articles" as directory_contents %}

{% for content in directory_contents %}

- [{{ content.title }}]({{ content.slug }})

{% endfor %}

## Tips

{% directory_contents "tips" as directory_contents %}

{% for content in directory_contents %}

- [{{ content.title }}]({{ content.slug }})

{% endfor %}
