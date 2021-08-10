from bs4 import BeautifulSoup
from .model import *
import urllib.parse
import re


def is_valid_tag(tag):
    return tag.name in ["h2", "h3", "p"] and tag.get('id') != "mw-toc-heading"


# Remove noise which is added by MediaWiki software, which we define to be references [###] or [edit] text. This will
# also strip out additional noise which is not useful to our use case (newlines and non-breaking spaces).
def strip_noise(text):
    return re.sub("(\\[[0-9]+])|(\\[edit])|(\n)|(\xe0)", "", text, flags=re.DOTALL)


def parse(content, url):
    article = BeautifulSoup(content, features="html.parser")

    # When we consider "sections", we will count only the primary headers (h2), which in Wikipedia's table of contents
    # correspond to the main numbered sections (1, 2, 3, ...). Subsections (h3) will be considered to be a part of the
    # main section, which is acceptable because, unlike sections, subsections do not follow a standard convention
    # on Wikipedia and tend to be an editorial choice.

    # In order to accurately parse just the text within the article itself (and not infoboxes or other visuals), we will
    # filter the page into the parts which directly contribute to article text (h2, h3, and p).
    # More complicated DOM like tables & lists require separate handling to parse accurately, which will not be dealt
    # with in this simple scraping tool (in order to keep this scraper easily understandable). One way of implementing
    # this could be through different "scraping strategies" based on the observed type of content, but this requires
    # more complicated analysis of each section and its surrounding elements. This is complicated by MediaWiki not using
    # containers or any types of additional HTML to semantically distinguish each section.
    contents = article.find_all(is_valid_tag)

    sections = []
    current_section = Section(title="Introduction", content="", links=[])
    for tag in contents:
        if tag.name == "h2":
            sections.append(current_section)
            current_section = Section(title=strip_noise(tag.text), content="", links=[])
        else:
            current_section.content += " "
            current_section.content += strip_noise(tag.get_text())
            # Extract all hyperlinks, normalizing them using urllib's urljoin() to ensure they are absolute URLs.
            for link in (map(lambda a: a['href'], tag.find_all(href=True))):
                current_section.links.append(urllib.parse.urljoin(url, link))

    return sections


