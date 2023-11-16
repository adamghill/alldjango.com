#!/usr/bin/env python

from os import getenv

from coltrane import initialize
from django.core.management import execute_from_command_line

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}


wsgi = initialize(
    GITHUB_PERSONAL_ACCESS_TOKEN=getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
    CACHES=CACHES,
)

if __name__ == "__main__":
    execute_from_command_line()
