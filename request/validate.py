import re

validation = re.compile("(https|http)://(..)\\.wikipedia\\.org/.*")


def is_wikipedia_url(url):
    return validation.match(url) is not None

