import httpx
from django import template
from django.conf import settings
from django.core.cache import cache
from django.utils.dateparse import parse_datetime
from glom import glom

register = template.Library()


def _get_stargazers(username: str) -> dict:
    cache_key = f"stargazers:{username}"

    if data := cache.get(cache_key):
        return data

    gql = """
query($username: String!) {
  user(login: $username) {
    login
    repositories(last: 100, orderBy: {field: STARGAZERS, direction: DESC}) {
      edges {
        node {
          name
          url
          stargazers(last: 100, orderBy: {field: STARRED_AT, direction: ASC}) {
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

    url = "https://api.github.com/graphql"

    headers = {"Authorization": f"token {settings.GITHUB_PERSONAL_ACCESS_TOKEN}"}

    res = httpx.post(
        url,
        json={"query": gql, "variables": {"username": username}},
        headers=headers,
        timeout=30,
    )

    res.raise_for_status()
    data = res.json()

    cache.set(cache_key, data, 30)

    return data


@register.simple_tag
def stargazers_by_repo_name(username: str) -> str:
    data = _get_stargazers(username)
    stargazers_by_repo_name = {}

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

    return stargazers_by_repo_name


@register.simple_tag
def last_stargazers(username: str):
    data = _get_stargazers(username)
    last_stargazers = []

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

    return last_stargazers


@register.filter
def str_to_date(s):
    return parse_datetime(s)
