from lxml.html import fromstring
import lxml.etree as etree


# TODO: check for author outside the parser when there is no isbn for the book
def check_for_author(author, orig_authors):
    if not orig_authors:
        return True
    author1 = orig_authors[0]
    authorsplit = author1.split(" ")
    author2 = author1
    if len(authorsplit) > 1:
        author2 = '%s %s'%(authorsplit[1], authorsplit[0])
    if author1.lower() not in author.lower() and strip_accents(author1) not in strip_accents(author) and author2.lower() not in author.lower() and strip_accents(author2) not in strip_accents(author):
        return False
    return True

def check_for_title(title, orig_title):
    if not orig_title:
        return True
    if orig_title.lower() not in title.lower() and strip_accents(orig_title) not in strip_accents(title):
        return False
    return True

def strip_accents(s):
    symbols = (u"öÖüÜóÓőŐúÚéÉáÁűŰíÍ",
                u"oOuUoOoOuUeEaAuUiI")
    tr = dict( [ (ord(a), ord(b)) for (a, b) in zip(*symbols) ] )
    return s.translate(tr).lower()



####

def parse_search_results(html_content):
    root = fromstring(html_content)
    results = root.xpath('//a[@class="book_selector"]')
    matches = set()
    for result in results:
        etree.strip_tags(result, 'strong')
        author = extract_author(result.text)
        title = extract_title(result.text)
        for url in result.xpath('@href'):
            matches.add((author, title, url))
    return matches


def extract_author(parsed_html):
    author_and_titles = parsed_html.split(':', 1)
    return author_and_titles[0].strip(' \r\n\t')


def extract_title(parsed_html):
    author_and_titles = parsed_html.split(':', 1)
    return author_and_titles[1].strip(' \r\n\t')
