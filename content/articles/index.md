---
template: base.html
title: Articles
---

# All Articles

{% current_directory_slugs as current_directory_slugs %}

{% for slug in current_directory_slugs %}

- [{{ slug.title }}]({{ slug.slug }})

{% endfor %}

- None yet
