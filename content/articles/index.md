---
template: base.html
title: Articles
description: A list of all articles.
---

{% directory_contents as articles %}
{% include '_contents.html' with contents=articles %}
