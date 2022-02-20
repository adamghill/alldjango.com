---
template: base.html
title: Tips
---

{% directory_contents as tips %}

{% for tip in tips %}
{% if not tip.draft %}
✨ [{{ tip.title }}]({{ tip.slug }})<br />
{% endif %}
{% endfor %}
