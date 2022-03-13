# alldjango.com

The website for alldjango.com. Built with Coltrane, sweat, blood, and tears.

# To build

`poetry run coltrane build`

# Color palette (such as it is)

https://coolors.co/8a4f7d-fbb13c-f0544f-20aa76-f4f6f6

# Promoted articles

## unique-urls

https://old.reddit.com/r/djangolearning/comments/sx78fy/prettier_urls_with_automatic_slug_generation/
https://twitter.com/adamghill/status/1495170037082112002?s=20&t=J3Eh18NuSncwfxot35GlPw

# To develop coltrane

1. `poetry remove coltrane-web`
1. Add `coltrane-web = { path="../coltrane", develop=true }` to `pyproject.toml`
1. `poetry lock && poetry install`
