import json
from hashlib import md5
from typing import Optional

import httpx
from django import template
from django.conf import settings
from django.core.cache import cache
from django.utils.dateparse import parse_datetime
from glom import glom

register = template.Library()


# Set the limit to 50 otherwise, the query times out
LIMIT = 50


class GqlError(Exception):
    def __init__(self, errors):
        error = errors[0]
        self.type = error.get("type")
        self.message = error.get("message")
        self.path = error.get("path")
        self.locations = error.get("locations")


def _hash(s: str) -> str:
    return md5(s.encode(), usedforsecurity=False).hexdigest()


def _get_gql(gql: str, variables: Optional[dict] = None) -> dict:
    if variables is None:
        variables = {}

    cache_key = _hash(gql)

    if variables:
        cache_key += _hash(json.dumps(variables))

    if data := cache.get(cache_key):
        return data

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
        raise GqlError(errors=data["errors"])

    cache.set(cache_key, data, 30)

    return data


def _get_stargazers(username: str) -> dict:
    gql = """
query($username: String!) {
  user(login: $username) {
    login
    repositories(isFork:false, last: 50, orderBy: {field: STARGAZERS, direction: ASC}) {
      edges {
        node {
          name
          url
          description
          stargazerCount
          defaultBranchRef {
            target {
              ... on Commit {
                history(first: 1) {
                  edges {
                    node {
                      ... on Commit {
                        commitUrl
                        committedDate
                      }
                    }
                  }
                }
              }
            }
          }
          stargazers(last: 50, orderBy: {field: STARRED_AT, direction: ASC}) {
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
            avatarUrl
          }
          ... on Organization {
            login
            avatarUrl
          }
        }
      }
    }
    followers(first: 100) {
      totalCount
      edges {
        node {
          login
          avatarUrl
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
    except httpx.HTTPStatusError as e:
        error = e
    except GqlError as e:
        error = e

    return (data, error)


@register.simple_tag
def stargazers_by_repo_name(username: str, repo_name: str) -> tuple:
    error = None

    try:
        data = _get_stargazers(username)
    except httpx.HTTPStatusError as e:
        error = e
    except GqlError as e:
        error = e

    result = {}

    for repository in glom(data, "data.user.repositories.edges"):
        repository_node = repository.get("node", {})

        name = repository_node.get("name")

        if repo_name != name:
            continue

        result.update(
            {
                "name": repository_node.get("name"),
                "url": repository_node.get("url"),
                "description": repository_node.get("description"),
                "stargazer_count": repository_node.get("stargazerCount"),
            }
        )

        commit_edges = glom(repository_node, "defaultBranchRef.target.history.edges")

        if commit_edges:
            commit_node = commit_edges[0].get("node", {})
            last_commit_date = commit_node.get("committedDate")
            last_commit_url = commit_node.get("commitUrl")

            result.update(
                {
                    "last_commit_date": last_commit_date,
                    "last_commit_url": last_commit_url,
                }
            )

        stargazers = []

        for stargazer in glom(repository, "node.stargazers.edges"):
            stargazer_node = stargazer["node"]

            if stargazer_node.get("login") == username:
                continue

            stargazer_node["starredAt"] = stargazer["starredAt"]
            stargazer_node["repo_name"] = repo_name
            stargazers.insert(0, stargazer_node)

        result["stargazers"] = stargazers

    return (result, error)


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

        last_stargazers = sorted(last_stargazers, key=lambda s: s.get("starredAt"), reverse=True)[:LIMIT]
    except httpx.HTTPStatusError as e:
        error = e
    except GqlError as e:
        error = e

    return (last_stargazers, error)


@register.filter
def str_to_date(s):
    return parse_datetime(s)


@register.simple_tag
def login_in_edge(login: str, data: dict) -> bool:
    if not login or not data:
        return False

    for edge in data.get("edges", []):
        if login == edge.get("node", {}).get("login"):
            return True

    return False
