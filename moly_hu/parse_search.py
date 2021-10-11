from lxml.html import fromstring
import lxml.etree as etree


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


def extract_author_and_title(result):
    author_n_title = result.text
    author_n_titles = author_n_title.split(':', 1)
    author = author_n_titles[0].strip(' \r\n\t')
    title = author_n_titles[1].strip(' \r\n\t')
    return author, title


def parse_search_results(html_content, orig_title=None, orig_authors=None):
    isbn = None

    root = fromstring(html_content)
    matches = set()
    exact_matches = set()

    results = root.xpath('//a[@class="book_selector"]')
    for result in results:
        book_urls = result.xpath('@href')
        matches.update(book_urls)
        if isbn is None:
            etree.strip_tags(result, 'strong')
            author, title = extract_author_and_title(result)
            if not check_for_title(title, orig_title) or not check_for_author(author, orig_authors):
                continue
        exact_matches.update(book_urls)

    return exact_matches or matches


def strip_accents(s):
    symbols = (u"öÖüÜóÓőŐúÚéÉáÁűŰíÍ",
                u"oOuUoOoOuUeEaAuUiI")
    tr = dict( [ (ord(a), ord(b)) for (a, b) in zip(*symbols) ] )
    return s.translate(tr).lower()
