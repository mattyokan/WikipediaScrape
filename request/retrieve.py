import requests
from . import headers
from . import validate


def retrieve_article(url):
    if not validate.is_wikipedia_url(url):
        raise RuntimeError("Destination {url} is not a Wikipedia article.".format(url=url))

    response = requests.request('GET', url, headers=headers.choose_header())

    if not response.ok:
        raise RuntimeError("Invalid response {status_code} from destination {url}.".format(
            status_code=response.status_code, url=url))

    return response
