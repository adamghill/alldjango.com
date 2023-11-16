# alldjango.com

The website for alldjango.com. Built with `Coltrane` and ☕️.

# Run locally

- Install `Poetry`
- `cp .env.example .env` and update `.env` with a secret key
- `poe r` or `poetry run coltrane play`

# To build static site

`poetry run coltrane build`

# Color palette (such as it is)

https://coolors.co/8a4f7d-fbb13c-f0544f-20aa76-f4f6f6

# To develop with local `Coltrane`

1. `poetry remove coltrane`
1. Add `coltrane = { path="../coltrane", develop=true }` to `pyproject.toml`
1. `poetry lock && poetry install`
