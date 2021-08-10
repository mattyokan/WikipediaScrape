from request import retrieve
from parse import parser
from analyze import frequency


def main():
    # could be redirected to user input easily, but this was not specified.
    frequency_count = 5
    url = input("Enter a Wikipedia article URL (e.g https://en.wikipedia.org/wiki/Bank_War):\n")
    try:
        response = retrieve.retrieve_article(url)
    except RuntimeError as ex:
        print(ex)
        return

    sections = parser.parse(response.content, url)
    print("Identified {count} sections.".format(count=len(sections)))

    for section in sections:
        print(f"Section {section.title}:")

        if len(section.links) > 0:
            print("  Hyperlinks:")
            for link in section.links:
                print(f"    {link}")
        else:
            print("    No links for this section.")

        words = frequency.most_frequent_stopwords(section.content, frequency_count)

        if words.size > 0:
            print(f"  Top {frequency_count} words in this section:")
            for word, count in words.items():
                print(f"    {word}: {count}")
        else:
            print("    No body text in this section.")


main()

