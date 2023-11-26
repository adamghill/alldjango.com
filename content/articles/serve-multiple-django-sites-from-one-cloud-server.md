---
template: base.html
title: Serve multiple Django sites from one cloud server
date: 2022-11-30 22:33:16 -0400
categories: django python docker
description: Run multiple Django projects on a $6/month Digital Ocean cloud server using CapRover.
---

I was a long time user of `Heroku`, but after they announced the removal of all of their free plans, I have started to look to move all of my side projects to other hosts. I don't begrudge them for wanting to focus on paying customers, but most of my side projects have very low traffic so their pricing tiers don't make much sense for me anymore.

Initially I moved most of my sites to [render](https://render.com). It is a delightful hosting platform very similar to Heroku, although you'll need to translate any custom `buildpacks` into the `render.yml` file, so it's not quite as simple a translation as I would like. However, `render` is easy to use and has a nice UI to provision services. I still have a few sites hosted there, mostly for their managed Postgres database support. I even have a [checklist](https://gist.github.com/adamghill/ba816554995d1fe5e5b2195ec76eaef8) I use to deploy sites to `render`.

However, for low traffic sites I have increasingly become enamored with [`CapRover`](https://caprover.com/) after [Tobi-De](https://github.com/Tobi-De) suggested it to me. `CapRover` can be hosted on lots of hosting platforms, but I have primarily used it on **Digital Ocean**. If you sign up for [Digital Ocean](https://m.do.co/c/617d629f56c0) you will get $200 in free credits (and full disclosure, I get a little credit for my hosting costs as well).

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=617d629f56c0&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

## Self-hosting `CapRover`

### Benefits

One major pro of using [`CapRover`](https://caprover.com/) is that you can use one server to host multiple sites at once. On Heroku or `render` each "service" will host one site by default. Free tiers will typically limit you to one free site, even for very low traffic sites. Sometimes services in the free tier will be "put to sleep" as well. On `CapRover`, I can host multiple Django apps on a $6/month server *and* they are fast and reliable.

Another pro is that `CapRover` has a long list of one-click installs for open source software. This includes backend services like `Postgres`, `mysql`, and `redis`. Complete packages are also available like analytics tracking ([`umami`](https://umami.is/) and [`ackee`](https://ackee.electerious.com/)), error monitoring ([`glitchtip`](https://glitchtip.com/)), or uptime monitoring ([`Uptime Kuma`](https://uptime.kuma.pet/)) are all one click away.

### Drawbacks

The major con is that support is mainly through GitHub Issues. However, the `CapRover` documentation is *pretty* good -- I did have to re-read some sections a few times to understand what to do, but overall it seems pretty solid. However, hopefully this tutorial lets you avoid some of the learning curve I went through.

One other con is that I have noticed a short time where my sites are unavailable while new code is getting deployed. According to [this comment](https://github.com/caprover/caprover/issues/661#issuecomment-619548552) `CapRover` does support zero-downtime deploys. For low traffic sites I'm not worried about a few seconds of downtime, but it is something to keep in mind.

### Other options

[dokku](https://dokku.com/) is another popular option for a self-hosted PaaS and is similar to `CapRover`, but it doesn't have an admin web UI. It does support `buildpacks` so if you are transferring from `Heroku` that might be helpful.

## How to create a server in the ☁️

### Sign up

There are lots of options for servers in the cloud, however the easiest one I have used with `CapRover` is **Digital Ocean**. [Sign up for an account](https://m.do.co/c/617d629f56c0) to get started.

### Create a project

A `project` holds related servers together. To make things easier, I just have one project that I put everything in.

### Create a server

**Digital Ocean** calls their cloud servers `droplets` (which is sort of adorable come to think of it).

1. Click the green *Create* button in the top navigation header
2. Click *Droplets* ![Create droplet]({% static 'img/deploy/digital-ocean-create-droplet.png' %})
3. Under *Choose an image*, click the *Marketplace* tab
4. Search for "caprover" in the *Search keyword* text box ![Search for CapRover]({% static 'img/deploy/digital-ocean-search-caprover.png' %})
5. Click *CapRover* in the search results that shows up ![Choose CapRover]({% static 'img/deploy/digital-ocean-choose-caprover.png' %})
6. Under *Choose a plan*, click *Basic*
7. In the *CPU options* radio button, click *Regular with SSD*
8. Click the *$6/mo* option; feel free to choose a more expensive option if you want -- you will be able to change this option later on if you want ![Choose a basic plan]({% static 'img/deploy/digital-ocean-choose-plan.png' %})
9. Under *Chose a datacenter region*, select a region close to you; I selected *New York*
10. Under *Authentication*, create an SSH key with `ssh-keygen` or `1Password` and copy the output of the public key in
11. Click the *Monitoring* checkbox under *Select additional options*
12. Put in a memorable name for your new server in the cloud in the text box under *Choose a hostname*
13. Click *Create Droplet*

It might take a few minutes, but eventually there will be an `ipv4` address on the `droplet` page. With that you can start setting up `CapRover`.

At this point, you *can* access `CapRover` by going to `droplet` IP address and a port of 3000, e.g. if your IP address was 123.456.789.123, then you could go to 123.456.789.123:3000. The default login is "captain42", but I suggest continuing on. The `CapRover` setup will prompt you to change the password in the next step.

## `CapRover` setup

### Subdomain

You can use any domain name for the `CapRover` instance. It doesn't need to be the site that you want `CapRover` to host. For example, let's say you have two domains, `boats-r-us.com` and `boats-and-totes.com`. Both will be `Django` projects that are deployed using `CapRover`. You could use either of those domains for the `CapRover` admin UI or *another* domain. For example, you might want to host `CapRover` on `boat-lovers.com`. It's up to you to decide for your situation.

You can do this in any DNS provider, but I tend to use `Cloudflare`. Other DNS providers should be a similar process.

1. Log into [Cloudflare](https://www.cloudflare.com/)
2. Click on the domain name you want to use for the `CapRover` admin UI, e.g. `boat-lovers.com`
3. Click on *DNS* in the sidebar
4. Click on *Add record*
5. Make sure that *Type* is "A"
6. Decide on a unique subdomain which will be the third-level domain where all `CapRover` services will be created -- this will require a wildcard fourth-level A name to be added; e.g. `apps` could be your third-level domain name for `boat-lovers.com` so an app named `boats-r-us` would live at `boats-r-us.apps.boat-lovers.com`
    a. Add the subdomain with the fourth-level wildcard to the *Name* text box; e.g. "*.apps"
7. Put the `ipv4` address for the `droplet` into the *IPv4 address* text box
8. Make sure the the *Proxy status* is un-checked, i.e. it is grey and says *DNS only*
9. Click *Save*

## Server setup

Run the following in your source code directory on your local machine.

1. `npm install -g caprover`
2. `caprover serversetup`
3. Follow the prompts, but make sure to use the third-level domain for your "root domain", e.g. `apps.boat-lovers.com`
4. Go to `captain.apps.boat-lovers.com` and login with the password you set to access the `CapRover` admin UI

## Deploy Django code

My [`docker-python-poetry-django` repository](https://github.com/adamghill/docker-python-poetry-django) has the files needed for `CapRover` to work correctly.

- `captain-definition`: tells `CapRover` where to find the `Dockerfile`
- `Dockerfile`: multi-stage definition for how the server should be setup to run the Django site; it installs dependencies via `poetry`, runs the `bin/post_compile` script for Django-specific management commands, and serves the site via `gunicorn`
- `bin/post_compile`: script to run `collectstatic`, `migrate`, etc.; can be customized for your particular application

>Make sure to update `ALLOWED_HOSTS` in your Django settings file to include the correct fourth-level domain name, e.g. `ALLOWED_HOSTS = ['boats-r-us.apps.boat-lovers.com']`.

1. `caprover deploy` from source code directory and follow the prompts
2. Go the the `CapRover` admin UI and click on *Apps* and then your app name
3. Click on the *Deployment* tab at the top
4. Click on *View Build Logs* if necessary and watch for errors
5. Go to your app's URL via the fourth-level domain name

## Public domain name setup

Now that your app works, you can provide a better public URL for people to access the site. A "naked" domain won't have a "www" in front of it. You can also create a *rule* in `Cloudflare` to redirect one type of domain to the other.

### first-level domain name

The first level domain can be either "naked" or a third-level domain name. A "naked" domain only has a first level domain name and a TLD, e.g. `boat-lovers.com`.

#### Naked

This will alias `boat-lovers.com` to `boats-r-us.apps.boat-lovers.com`.

1. Log into [Cloudflare](https://www.cloudflare.com/)
2. Click on the domain name you want to use, e.g. `boat-lovers.com`
3. Click on *DNS* in the sidebar
4. Click on *Add record*
5. Make sure that *Type* is "A"
6. Put "@" in for the *Name*
7. Put the *droplet* `ipv4` address into the *IPv4 address* text box
8. Make sure the the *Proxy status* is checked
9. Click *Save*

#### www

This will alias `www.boat-lovers.com` to `boats-r-us.apps.boat-lovers.com`.

1. Log into [Cloudflare](https://www.cloudflare.com/)
2. Click on the domain name you want to use, e.g. `boat-lovers.com`
3. Click on *DNS* in the sidebar
4. Click on *Add record*
5. Make sure that *Type* is "CNAME"
6. Put "www" in for the *Name*
7. Put the app's URL into the *Target* text box
8. Make sure the the *Proxy status* is checked
9. Click *Save*

### Add the domain name

1. Log into your `CapRover` instance, e.g. `captain.apps.boat-lovers.com`
2. Click on *Apps* in the sidebar
3. Click on the name of your app in the list
4. In the *HTTP Settings* tab, underneath of *Your app is publicly available at:*, add either the naked domain or the "www" domain (or both), e.g. `boats-r-us.com` or `www.boats-r-us.com`
5. Click *Connect New Domain*
6. Once all domains are added, click *Enable HTTPS* for each one (even though this seems unnecessary since `Cloudflare` provides free SSL as well)

## Automatic deploys

Once manual deploys are working, you can set up `CapRover` to deploy a new version of your code every time you push to a specific branch in your repository.

The first option is to set up a webhook from GitHub that calls `CapRover` and `CapRover` builds the Docker image. The second option is to use a GitHub Action to build the Docker file and push the image to your `CapRover` installation.

### `CapRover` builds the Docker image

The benefit of having `CapRover` build your Docker image is that it is less hassle to setup and the output of building the Docker image is in the `CapRover` UI. The downside is building the Docker image can use a lot of CPU and memory on your server.

#### Generate the keys for deploys

Generate a *private key* and *public key* in the same directory as your code.

```shell
ssh-keygen -t ed25519 -C "skiff@boat-lovers.com" -f ./deploykey -q -N ""
```

A *private key* (named `deploykey`) and a *public key* (`deploykey.pub`) will be created in the current directory.

#### Add the public key to GitHub

1. Create a deploy key in GitHub by going to `https://github.com/USERNAME/REPOSITORY_NAME/settings/keys/new`
2. Give the key a *Title* (e.g. "CapRover") 
3. Paste the contents of `deploykey.pub` into the *Key* text field
4. Do not check *Allow write access* unless you have a good reason to
5. Click *Add key*

#### Add the private key to `CapRover`

Go to the *Deployment* tab for your app in `CapRover`. Scroll down to *Method 3: Deploy from Github/Bitbucket/Gitlab*.

1. Type your GitHub repo into *Repository*
2. Put the branch you want to automatically deploy into *Branch* (typically either "main" or "master")
3. Paste the contents of the `deploykey` file into the text field underneath of *Or, instead of username/password, use SSH Key:*
4. Make sure there is a blank line at the bottom of the pasted contents otherwise GitHub won't validate it
4. Click *Save & Update*
5. The text box above *Repository* should now have a long URL inside of it; copy that into your clipboard

#### Add the webhook to GitHub

1. Go to https://github.com/USERNAME/REPOSITORY/settings/hooks/new and paste the generated URL from the last step into the *Payload URL* text box; leave the rest of the settings as-is
2. Click *Add webhook*

Now when you push commits to the branch you specified:
1. GitHub calls the webhook
2. `CapRover` pulls the new code from GitHub
3. `CapRover` builds the *Dockerfile*
4. `CapRover` deploys the site

### GitHub Action builds the Docker image

The benefit of having a GitHub Action build your Docker image is that the process will not steal resources from other applications running on your *droplet*.

#### Create GitHub personal access token

1. Go to the [Personal access tokens page on GitHub](https://github.com/settings/tokens)
2. Click *Generate new token (classic)*
3. Type something like "CapRover Docker repository" for the *Note*
4. Set *Expiration* to *No expiration*
5. Select *read:packages* checkbox
6. Click *Generate token*
7. Copy token to clipboard

#### Add Docker registry to `CapRover`

![CapRover Docker Registry]({% static 'img/deploy/caprover-docker-registry.png' %})

1. Go `CapRover` admin UI
2. Click *Cluster* in the left-hand navigation
3. Click *Add Remote Registry*
4. Put your GitHub username in *Username*
5. Put the generated GitHub token from above in *Password*
6. Type "ghcr.io" for the *Domain*
7. Click *Add Remote Registry*

#### Create `CapRover` app token

1. Go `CapRover` admin UI
2. Click *Apps* in the left-hand navigation
3. Click the application you want to set up
4. Click the *Deployment* tab
5. Go to the *Method 1: Official CLI* sub-header
6. Click *Enable App Token*
7. Copy the generated app token

#### Add secrets for the GitHub Action

1. Go to https://github.com/USERNAME/REPOSITORY_NAME/settings/secrets/actions
2. Click *New repository secret* and type "CAPROVER_APP_TOKEN" into *Name* and the generated app token from the last step into *Secret*; click *Add secret*
3. Click *New repository secret* and type "CAPROVER_SERVER_URL" into *Name* and the URL for your `CapRover` server into *Secret*; click *Add secret*

#### Add the GitHub Action

This GitHub Action will build the Docker image and push to `CapRover` when code is pushed to the `main` branch.

1. Go to https://github.com/USERNAME/REPOSITORY_NAME/actions
2. Click *New workflow*
3. Click *set up a workflow for yourself*
4. Name the workflow "deploy-to-caprover.yml" or something similar
5. Copy the following into the YAML file
```yaml
on:
  push:
    branches:
      - main

jobs:
  deploy-to-caprover:
    name: Deploy to CapRover
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:
      - uses: adamghill/build-docker-and-deploy-to-caprover@2.3.0
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          caprover-app-name: YOUR-APP-NAME
          caprover-server-url: ${{ secrets.CAPROVER_SERVER_URL }}
          caprover-app-token: ${{ secrets.CAPROVER_APP_TOKEN }}
```
6. Click *Commit changes...*
7. Click the *Actions` sub-navigation to see the workflow run

#### Make sure Actions have the right permissions

1. Got to https://github.com/USERNAME/REPOSITORY_NAME/settings/actions
2. Go to the *Workflow permissions* section
3. Click the *Read and write permissions* radio button
4. Click *Save*

![Create droplet]({% static 'img/deploy/action-workflow-permissions.png' %})

## Custom Dockerfile per app

For one of my side projects, [devmarks.io](https://devmarks.io), there is a web site and a worker process and they share the same code. I have two apps in `CapRover`, one named `devmarks-web` and another named `devmarks-worker`. Typically my [`Dockerfile`](https://github.com/adamghill/docker-python-poetry-django/blob/main/Dockerfile#L45) calls a [script](https://github.com/adamghill/docker-python-poetry-django/blob/main/bin/post_compile) that runs `collectstatic` and a few other management commands and then runs [`gunicorn`](https://github.com/adamghill/docker-python-poetry-django/blob/main/bin/post_compile#L19). However, for my worker app I don't need `collectstatic` to run and instead of `gunicorn` I would like to start the worker process.

`CapRover` allows per-app changes to the `captain-definition` file. So, for `devmarks-worker` I created a `captain-definition-worker` file that references a new `Dockerfile-worker` file. The only difference in `Dockerfile-worker` is the  `CMD` statement at the end which calls `python manage.py qcluster`.

1. Go to your app in the `CapRover` admin UI
2. Click the *Deployment* tab
3. Scroll to the bottom to the *captain-definition Relative Path* textbox
4. Click `Edit`
5. Type in `./captain-definition-worker` and click *Save & Update*

Now when `CapRover` starts up the container it will use `captain-definition-worker` and `Dockerfile-worker` to start up my worker process.

## Cron jobs

I have a few cron jobs that I need to run that are currently Django management commands.

[Cron + Docker = The Easiest Job Scheduler You’ll Ever Create](https://levelup.gitconnected.com/cron-docker-the-easiest-job-scheduler-youll-ever-create-e1753eb5ea44) seems useful if your cron jobs are independent of your code. [Chadburn](https://github.com/PremoWeb/Chadburn) is a one-click install for `CapRover` and seemingly helps manage cron tasks, but it is contained with its own container. However, my cron jobs need to either 1) be in the same Docker instance as my code, or 2) be able to call *into* the Docker container.

Setting up cron *inside* my Docker container with my source code would mean that *every* instance would run the cron jobs, potentially duplicating the cron jobs when more than one instance of my app was running. That didn't seem ideal.

### Manually setup cron jobs

One option is to specify the cron jobs in the `droplet` that contains all of my containers. It feels a little messy, but I will document them in my code repository to try to mitigate that. This solution works because from the `droplet` I can call into any `CapRover` app I want.

```shell
docker exec -it $(docker ps --filter name=srv-captain--APP_NAME -q) python manage.py MANAGEMENT_COMMAND
```

I think theoretically this should work, but I could never figure out why my cron jobs never ran. I'm sure I was missing some straight-forward Linux-y thing, but I tried troubleshooting off and on and never did figure out what was going on.

### Queues with scheduled tasks

Eventually I decided to investigate queues that integrate with Django *and* support scheduled tasks.

I evaluated:
- [`django-rq-scheduler`](https://django-rq-scheduler.readthedocs.io/)
- [`huey`](https://huey.readthedocs.io/)
- [`django-q2`](https://django-q2.readthedocs.io/)
- [`Celery`](https://docs.celeryq.dev/)

After trying each option out, I have landed on using `django-q2`. For me, it was the best mix of Django integration, low resource use, and understandable to debug.

## Troubleshooting `CapRover`

At one point, I broke the `CapRover` admin UI because of an SSL issue. I ended up looking through the logs and restarting the `CapRover` instance to fix it.

### Logging into the `droplet`

Log into **Digital Ocean** and click the *Console* button for your `droplet`. ![Digital Ocean Console]({% static 'img/deploy/digital-ocean-console.png' %})

### View logs

```shell
docker service logs srv-captain--APP_NAME --since 60m --follow
```

### Restart `CapRover`

```shell
docker service update captain-captain --force
```

### See all running apps

```shell
docker ps
```

### Run Django management command

Get the `Docker` container id from the `ps` command above and use it with `docker exec`.

```shell
docker exec -it CONTAINER_ID python manage.py MANAGEMENT_COMMAND
```

Or to run a command by the `CapRover` app name.

```shell
docker exec -it $(docker ps --filter name=srv-captain--APP_NAME -q) python manage.py MANAGEMENT_COMMAND
```

### Domain Verification Failed - Error 1107

Enabling HTTPS for a domain is usually painless, but one time I kept getting a validation error for an extended period. I double-checked that the new IP and domain were set properly in Cloudflare multiple times and waited a few hours, but it never worked. However, you can skip domain verification if needed.

1. Log into [Digital Ocean](https://www.digitalocean.com)
2. Go to your *droplet*
3. Click on the *Console* button
4. Copy the following into the terminal and pretty Enter
```
echo  "{\"skipVerifyingDomains\":\"true\"}" >  /captain/data/config-override.json
docker service update captain-captain --force
```
5. Wait a few minutes for `CapRover` to restart
6. Try to enable HTTPS for your app again and hopefully it will work

### Postgres 15 permission error

This is not about CapRover, but Postgres 15 has changed how permissions are created for database users. For every new project, I tend to create a new database, user, and PG Bouncer pool. However, for Postgres 15 I would see an error about "Can't create tables in public schema" for `django_migration`. I had to explicitly give permission to my new user to change the new database.

```shell
PGPASSWORD=PASSWORD psql -U doadmin -h DATABASE_URL -p PORT -d DATABASE_NAME --set=sslmode=require -c "ALTER DATABASE DATABASE_NAME OWNER TO DATABASE_USER;"
```

### NetData missing container statistics

I keep a close eye on the **Digital Ocean** `droplet` and `Postgres` statistic graphs to make sure the server is healthy and working correctly. `CapRover` also includes the `NetData` monitoring tool which has some more detailed statistics. However, my individual Docker container statistic were not showing. To fix this log into your droplet and run the following to update the version of `NetData`.

```
echo  "{\"netDataImageName\":\"caprover/netdata:v1.34.1\"}" >  /captain/data/config-override.json
docker service update captain-captain --force
```

## Conclusion

Hopefully this has been helpful for anyone who wants to host a Django site (or a few!) relatively inexpensively. Just a reminder if you sign up for [Digital Ocean](https://m.do.co/c/617d629f56c0) with my referral code you will get $200 in free credits (and my undying appreciation!).

## More resources, documentation, and details

- [`CapRover` documentation](https://caprover.com/docs/get-started.html)
- [`CapRover` service override](https://caprover.com/docs/service-update-override.html)
- [`bash` strict mode](https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425)
- [Docker setup](https://github.com/Tobi-De/fuzzy-couscous/tree/main/project_name/docker) by [Tobi-De](https://github.com/Tobi-De)
- [Docker multi-staged builds](https://github.com/michaeloliverx/python-poetry-docker-example/) by [michaeloliverx](https://github.com/michaeloliverx)
- [Explanation of Docker](https://fastapi.tiangolo.com/deployment/docker/) by [Tiangolo](https://github.com/tiangolo)
- More information about [GitHub deploy keys](https://github.com/caprover/caprover/issues/1265#issuecomment-973651341)
- More details about [NetData missing container statistics](https://github.com/caprover/caprover/issues/1522)
- [How to Deploy Django using CapRover](https://justdjango.com/blog/deploy-django-caprover)
- [The Essential Django Deployment Guide](https://www.saaspegasus.com/guides/django-deployment/)
