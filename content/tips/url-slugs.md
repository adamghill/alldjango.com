---
template: base.html
title: URL Slugs
---

# URL Slugs

When building a website, lots of times you will need to expose some information from the database for a row of data. For example, if you have an e-commerce site which lists products for sale, you might have URLs like https://www.djangozon.com/products/really-cool-products.

the `DetailView` is the generic class-based views is

## One last note

Another approach that sites like StackOverflow use is to try to have their cake and eat it, too. Look at an example URL closely and you will see a unique identifier AND a slug: https://stackoverflow.com/questions/34230208/uuid-primary-key-in-postgres-what-insert-performance-impact. The slug at the end isn't used to look up the question at all. The integer is the identifier and if the question that is looked up has a different slug than the last part of the URL, they redirect the url so the slug is correct. It is one way to have nicer looking URLs, but also a canonical identifier. The same approach would work if you don't want the integer identifier exposed.
