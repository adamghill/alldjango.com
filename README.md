# alldjango.com

The website for alldjango.com. Built with Coltrane, sweat, blood, and tears.

# To build

`poetry run coltrane build`

# Color palette (such as it is)

https://coolors.co/8a4f7d-fbb13c-f0544f-20aa76-f4f6f6

# To develop coltrane

1. `poetry remove coltrane-web`
1. Add `coltrane-web = { path="../coltrane", develop=true }` to `pyproject.toml`
1. `poetry lock && poetry install`
