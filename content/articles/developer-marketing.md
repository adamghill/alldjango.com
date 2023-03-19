---
template: base.html
title: Marketing for Developers
date: 2023-02-26 10:20:16 -0500
categories: django python
description: How to promote your open-source library as a developer to other developers.
---

I can sometimes view the world in idealistic ways. I _want_ to believe in meritocracy and that marketing is unnecessary, but even for developer tools, marketing is necessary for people to find and use your code. Writing the code and clicking the `Public` radio button when creating the repo in GitHub is just the first step.

Here is a list of other steps to make sure that others discover your code, use it, and contribute back. Not every suggestion is necessary and they are roughly sorted from easiest to hardest to implement.

I mostly know the Django ecosystem, so that's what I focused on, but I'm sure other programming languages have analogous approaches.

## Make the repo public

You made a thing! That's awesome! Make sure it's `public`, otherwise your code will just sit around being sad and lonely.

Give your repo a succinct, but descriptive tagline so people know what it is. Then add tags to the repo so your repo can be found easier when searching in GitHub.

## Create a `README.md`

First impressions matter for code just like everything else. Only the most die-hard developer will delve through your code without some basic information. The least you can do is create a `README.md` in the root directory and include things like:

- a longer description of what your library does
- a list of features
- installation instructions

If you really want a stellar `README.md` take a look at some of the examples in [awesome-readme](https://github.com/matiassingers/awesome-readme) for inspiration!

## Submit your library

There are a few websites where you can easily submit your library for others to find.

- [Django Packages](https://djangopackages.org/): the O.G. site to find libraries for Django.
- [libhunt](https://python.libhunt.com/): a list of Python open-source projects; submitting here will sometimes get you included in the [Awesome Python newsletter](https://python.libhunt.com/newsletter).
- [awesome-django](https://awesomedjango.org/): a curated list of awesome Django projects; submit your own by making a [PR](https://github.com/wsvincent/awesome-django).

## GitHub Discussions

Creating posts in GitHub Discussions are an easy to way to engage with the community. Personally, I have found it's hard to generate a lot engagement in here, but maybe with bigger projects or a more deliberate strategy it could be a valuable tool.

One thing I _have_ experimented with in some repositories is disabling the creation of `GitHub Issues` and using `Discussions` for that instead. One thing I like about this approach is it allows users to engage in a way that feels less aggressive. A user is not creating a problem for you to solve, they are creating a topic to talk through.

## Write blog posts

Writing a blog posts is definitely marketing! Write about why you created your library, the challenges you overcome, lessons you learned, or tutorials for how to use the library.

[dev.to](https://dev.to/) and [Medium](https://medium.com/) are good places to post technical articles which have some built-in search and promotion capabilities so others can find your writing.

## Social media

Twitter and Mastodon have technical audiences, but you will get more traction once you have more followers. Be generally helpful to the community and learn to use these tools that isn't against the grain. Also, use hashtags in Mastodon when posting to increase the odds that others will find it.

Some sub-reddits also have technical audiences, but reddit seems to be less tolerant of self-promotion. Again, the more active and helpful in these communities you are, the more tolerant they will be. I have also mentioned my tool at the end of an answer for relevant questions -- but always provide help first.

The official [Django Forums](https://forum.djangoproject.com/) has a specific `Show & Tell` section. I have used it before, but it doesn't seem to be as active as the [Django sub-reddit](https://www.reddit.com/r/django/) in my opinion.

GitHub is also technically a "social platform" so other developers will follow you there. It's much more passive, though so you cannot directly message them. They will see notifications when you do certain actions. You _can_ send updates to GitHub Sponsors via email if that's something you end up doing.

I've never set up an email newsletter, but that would be another way to "own" the relationship with users without relying on a third-party like Twitter.

In general, don't be overbearing and do not be spammy and it will usually be ok.

## Create a documentation site

After you have created  a rad `README.md` you might notice it gets pretty long with numerous sections. This will be especially true for any library with lots of functionality. Breaking up the `README.md` into multiple pages can help with organizing the content.

[`Sphinx`](https://www.sphinx-doc.org/) is the go-to tool for documentation. It took me a while to understand how to use `Sphinx`, but I now have a decent workflow with `MyST` which allows me to write all the docs in `markdown`. My [sphinx-markdown-docs repo](https://github.com/adamghill/sphinx-markdown-docs) shows an example of what I do.

[ReadTheDocs](https://readthedocs.org/) is a free way to host your open-source documentation.

[diataxis](https://diataxis.fr/) is a systematic framework for technical documentation authoring which I keep meaning to read through more carefully and implement. It might be useful as you build out your own documentation to keep it in mind.

## Create screencasts

Some people learn better visually and some libraries greatly benefit from being shown. Animated gifs or short mov files can be especially useful for simple interactions. I use [Kap](https://getkap.co/) (free) to create these simpler screenshares.

For longer screencasts I have used [Screenflick](https://www.araelium.com/screenflick-mac-screen-recorder) (currently $35 one-time fee). It allows you to only capture a portion of the screen or a whole application, record audio, includes some simple editing capabilities, etc. There are some free options (e.g. OBS), but I found them difficult to setup and deal with. `Screenflick` was easy to use and totally worth the one-time fee.

Personally, creating a compelling screencast takes me a long time: deciding what to showcase, creating the sample code, writing a (loose) script. With practice I'm sure this goes faster, or if you are used to podcasting or streaming already.

## Go on podcasts

Once you've hit influencer status 🫣 you might get invited to go on a podcast to talk about your library. Podcasts are great to "get the word out" and "brand awareness", however most people are listening to podcasts in their car, doing the dishes, etc. Make it compelling and provide easy calls to action for people to re-find you or the library once they get back to a computer.

## Give a conference talk

Most conferences will not accept a long talk strictly about your library, however, making a talk about a general problem or a specific technical solution that is applicable is always welcome. Mentioning your library as part of the conference talk will be ok. Some talks can just be about being seen as a go-to resource in the community, as well.

Creating a conference talk is _hard_. My one and only real conference talk took 40-60 hours to create and record. Not for the faint of heart, but it is a good experience to do at least once in my opinion.

Shorter "lightning" or "attendance" talks are another approach. They are usually in the 5-15 minute range so are much more focused, just stressful, and talking about a specific tool seems ok in this context.

## In summary

Creating a repository that others know about and will use is way more involved than just writing code and it requires _some_ marketing from the developer. Hopefully this provided some ideas about how to promote your awesome library and help people find what you make!
