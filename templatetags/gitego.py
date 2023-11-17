import json
from hashlib import md5

import httpx
from django import template
from django.conf import settings
from django.core.cache import cache
from django.utils.dateparse import parse_datetime
from glom import PathAccessError, glom

register = template.Library()


def _get_gql(gql: str, variables: dict = None) -> dict:
    if variables is None:
        variables = {}

    cache_key = md5(gql.encode(), usedforsecurity=False).hexdigest()

    if variables:
        cache_key += md5(json.dumps(variables).encode(), usedforsecurity=False).hexdigest()

    if data := cache.get(cache_key):
        # return data
        pass

    url = "https://api.github.com/graphql"

    headers = {"Authorization": f"token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}"}

    res = httpx.post(
        url,
        json={"query": gql, "variables": variables},
        headers=headers,
        timeout=30,
    )

    res.raise_for_status()
    data = res.json()

    if "errors" in data:
        raise Exception(data["errors"][0])

    cache.set(cache_key, data, 30)

    return data


def _get_stargazers(username: str) -> dict:
    gql = """
query($username: String!) {
  user(login: $username) {
    login
    repositories(isFork:false, last: 100, orderBy: {field: STARGAZERS, direction: ASC}) {
      edges {
        node {
          name
          url
          stargazers(last: 100, orderBy: {field: STARRED_AT, direction: ASC}) {
            totalCount
            edges {
              starredAt
              node {
                login
                name
                avatarUrl
              }
            }
          }
        }
      }
    }
  }
}
"""

    data = _get_gql(gql, variables={"username": username})

    return data


def _get_user(username: str) -> dict:
    gql = """
query($username: String!) {
  user(login: $username) {
    login
    avatarUrl
    websiteUrl
    hasSponsorsListing
    repositories {
      totalCount
    }
    followers {
      totalCount
    }
    following {
      totalCount
    }
    starredRepositories {
      totalCount
    }
    sponsoring {
      totalCount
    }
    sponsors(first: 100) {
      totalCount
      edges {
        node {
          ... on User {
            login
          }
          ... on Organization {
            login
          }
        }
      }
    }
  }
}
"""

    data = _get_gql(gql, variables={"username": username})

    return data


@register.simple_tag
def get_user(username: str) -> dict:
    error = None
    data = {}

    try:
        data = _get_user(username)
        data = glom(data, "data.user")

        sponsors = []
        for sponsor_node in data["sponsors"]["edges"]:
            try:
                sponsors.append(glom(sponsor_node, "node.login"))
            except PathAccessError as e:
                pass

        data["sponsors"] = sponsors
    except httpx.HTTPStatusError as e:
        error = e

    return (data, error)


@register.simple_tag
def stargazers_by_repo_name(username: str) -> tuple:
    stargazers_by_repo_name = {}
    error = None

    try:
        data = _get_stargazers(username)
    except httpx.HTTPStatusError as e:
        error = e

    for repository in glom(data, "data.user.repositories.edges"):
        add_repository = True

        for stargazer in glom(repository, "node.stargazers.edges"):
            if add_repository:
                # This is weird, but want to avoid including repos with no stargazers
                repo_name = repository["node"]["name"]
                stargazers_by_repo_name[repo_name] = []
                add_repository = False

            stargazer_data = stargazer["node"]

            if stargazer_data.get("login") == username:
                continue

            stargazer_data["starredAt"] = stargazer["starredAt"]
            stargazer_data["repo_name"] = repo_name

            stargazers_by_repo_name[repo_name].insert(0, stargazer_data)

    return (stargazers_by_repo_name, error)


@register.simple_tag
def last_stargazers(username: str) -> list[str]:
    last_stargazers = []
    error = None

    try:
        data = _get_stargazers(username)

        for repository in glom(data, "data.user.repositories.edges"):
            repo_name = repository["node"]["name"]

            for stargazer in glom(repository, "node.stargazers.edges"):
                stargazer_data = stargazer["node"]

                if stargazer_data.get("login") == username:
                    continue

                stargazer_data["starredAt"] = stargazer["starredAt"]
                stargazer_data["repo_name"] = repo_name

                last_stargazers.append(stargazer_data)

        last_stargazers = sorted(last_stargazers, key=lambda s: s.get("starredAt"), reverse=True)[:100]
    except httpx.HTTPStatusError as e:
        error = e

    return (last_stargazers, error)


@register.filter
def str_to_date(s):
    return parse_datetime(s)
