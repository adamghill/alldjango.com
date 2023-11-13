---
template: base.html
title: Python Package Manager Comparison 📦
date: 2023-11-12 22:10:16 -0400
categories: python packaging poetry rye hatch pdm
description: Comparing the different Python package managers in 2023.
draft: false
---

>This article started as a random thought and then [this post](https://indieweb.social/@adamghill/111395305035092074) on Mastodon.

>If you haven't read [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) from 2020, it is a good companion to this article and [apparently will be a released as a book in 2024](https://www.oreilly.com/library/view/hypermodern-python-tooling/9781098139575/).

# Introduction

It feels like Python packaging has changed pretty substantially over the past few years. When I started creating Python packages the preferred approach was with `setup.py` and (what felt like) a myriad of other random files that were needed like `MANIFEST.in`, `setup.cfg`, etc. I basically found a guide once and then copied and pasted files around once I seemed to get something working.

I was an early adopter of [`pipenv`](https://pipenv.pypa.io/) with the primary appeal being lock files which promised consistent deployments. My early excitement got me burned multiple times and I looked around some more.

I remember [`Poetry`](https://python-poetry.org) being the cool, new upstart at the time. It completely eschewed `setup.py`, `requirements.txt`, and other disparate files -- it had one `pyproject.toml` file to configure a project, developer-friendly tooling to add dependencies, a lock file for consistent deployments, and an algorithm to make sure that a tree of dependencies was all compatible with each other (which was not possible with that version of `pip` at that time).

I was in love. There were  definite rough patches and there were a few bugs that caught me here or there, but overall `Poetry` has been my go-to for a while.

However, in the past few years, `Python` packaging seems to be going through a new era of innovation. `pip` [released a dependency resolver in 2020](https://pip.pypa.io/en/latest/user_guide/#changes-to-the-pip-dependency-resolver-in-20-3-2020) that now complains when dependencies conflict. Also in 2020, [PEP 621](https://peps.python.org/pep-0621/) and [PEP 631](https://peps.python.org/pep-0631/) standardized `pyproject.toml` as the new normal for Python packages instead of `setup.py`. [PEP 517](https://peps.python.org/pep-0517/) and [PEP 660](https://peps.python.org/pep-0660/) created standards for Python build systems.

Based on those PEPs, `Poetry` isn't the only forward-thinking package manager anymore. `pipenv` is still around (and I presume more stable at this point!), but [`Hatch`](https://hatch.pypa.io/), [`PDM`](https://pdm-project.org/), and [`Rye`](https://rye-up.com) all promise a pleasant developer experience when creating Python packages.

# Benefits

Most of these package managers are of the "all in one" mentality and provide similar benefits: adding dependencies from the command-line, lock files, building, and publishing packages. If you want to do this manually [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) lays out the steps necessary. Reducing the number of tools required to create new Python packages means there is only one place to look for documentation and keep up to date.

# [Poetry](https://python-poetry.org)

My first modern Python package manager. I would say the documentation is still the best available, although it might be too "designed" for some. It does *a lot* -- maybe too much? -- but, in my opinion, it pioneered a lot of features that are now expected in other Python package managers. I get the feeling it sometimes pushes forward without waiting for official PEPs, although I think that has changed over the past few years.

One annoying feature lacking in `Poetry` that is available in every other option is the ability to define "scripts". For example, `poetry run dev` as an alias for `poetry run manage.py runserver 0:8000`. That is not available in standard `Poetry`, although I use [`poethepoet`](https://github.com/nat-n/poethepoet) (a `Poetry` plugin) to provide that functionality.

# [Hatch](https://hatch.pypa.io/)

`Hatch` never deviates from the Python PEP standards and brings a few innovative features to the table, including being able to group dependencies and scripts into custom [environments](https://hatch.pypa.io/latest/environment/). The [`hatch new [project]`](https://hatch.pypa.io/latest/intro/#new-project) command is surprisingly opinionated has settings for `ruff` (my new favorite Python tool), `pytest`, and `coverage`. I'm here for all of the tool choices, but I would be lying if I did not say it was a little surprising.

Under the PyPA GitHub organization which probably gives it more of a sheen of officialdom than other tools.

# [PDM](https://pdm-project.org/)

`PDM` for some reason feels like the sleeper option compared to the rest. I have not used it too much other than to set up a new project and play around with it a little bit. [Dan Sloan chimed in on Mastodon](https://fosstodon.org/@LucidDan/111401652323465954) pointed out that `PDM` follows all PEP standards, good cross-platform lock files, and a useful `pdm export` to output a standard `requirements.txt` file.

# [Rye](https://rye-up.com)

`rye` seems to have had a quick and meteoric rise. It was developed by the creator of Flask, [Armin Ronacher](https://github.com/mitsuhiko), based on his opinionated approach to building `Python` packages. It reminds me of `black` a little bit in which a respected `Python` developer made an opinionated tool and it caught fire in the community. `Rye` has an [overview of its philosophy](https://rye-up.com/philosophy/).

`Rye` has multiple notes that it is experimental and not production-ready, although I did not see any glaring issues with my simple testing. `Rye` is a little different than the other options because it mostly consolidates a set of other tools (`pip`, `pip-tools`, etc) into a particular workflow. Another is that it handles Python versions directly -- `Poetry` recommends using `pyenv` to deal with multiple Python environments.

# GitHub Stats

GitHub stats are not particularly useful, but the number of stars do give some indication of the community engagement with a particular tool (current as of 2023-11-12).

<img src="{% static 'img/python-package-manager-star-history-20231112.png' %}" />

# Conclusions and takeaways

Personally I have multiple libraries using `setup.py` and `Poetry`, one using `Hatch`, and now one using `Rye`. The next one might use `PDM`. 😎 I like trying new tools to see how they work and to improve my workflow.

One could look at all of the options for Python packaging and be frustrated by the [paradox of choice](https://en.wikipedia.org/wiki/The_Paradox_of_Choice). I understand that viewpoint, but I also appreciate that all of these tools are making different trade-offs and pushing the state of the art forward in their own ways. Maybe at some point in the future there will be one "approved" Python package manager ala `NPM` or `Cargo`, but I am doubtful. There are pros and cons with multiple options, but I tend to think its useful overall.

I personally have not used each package manager extensively. But, I have started a new project from scratch with each, did some simple tasks, and read through all of the documentation. Each project is relatively mature, so you can just choose any of the options and you would be fine. Standardizing on `pyproject.toml` means that the conversion from one package manager to another is usually just updating some `TOML`. So, choose the package manager that speaks to you (or try them all!) and improve your developer experience henceforth. 🛠️
