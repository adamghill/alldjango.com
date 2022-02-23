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

<br />

# Hi, I'm Adam 👋

> I've been a backend programmer for ~20 years in a variety of different languages before I discovered Python 10 years ago and never looked back. `alldjango` includes all the hard-won experience I've gained over the years building production-scale Django websites.

> Feel free to reach out to [me on Twitter](https://twitter.com/adamghill) with questions, comments, or bitter invectives.

## Side projects I've built

- [devmarks.io](https://devmarks.io/): Bookmarking for Developers
- [Unicorn](https://www.django-unicorn.com): A full-stack component library for Django 🦄
- [coltrane](https://coltrane.readthedocs.io/): A simple content site framework that harnesses the power of Django without the hassle 🎵
- [python-utils.com](https://www.python-utils.com/): The online playground for Python utilities
- [django-fbv](https://django-fbv.readthedocs.io/): Utilities to make Django function-based views cleaner, more efficient, and better tasting
- [unsuckjs.com](https://unsuckjs.com/): Progressively enhance HTML with lightweight JavaScript libraries
- [minestrone](https://minestrone.readthedocs.io/): An opinionated Python library that lets you search, modify, and parse messy HTML with ease 🥫

### `alldjango` inspiration

This project is extremely indebted to the ethos (and design!) of [boringrails.com](https://boringrails.com) by [Matt Swanson](https://twitter.com/_swanson). Check it out if you love 💎 more than 🐍.
