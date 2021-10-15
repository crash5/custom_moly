import pprint

import moly_hu.parser as parser
import moly_hu.parse_search as booksearch


def moly_book_details():
    with open('moly_hu/test/hu_series.html', 'r') as f:
        return parser.HtmlParser().extract_book_details(f.read())


def moly_search_results():
    with open('moly_hu/test/search_multiple_book.html', 'r') as f:
        return booksearch.parse_search_results(f.read())


if __name__ == "__main__":
    print('Start...')
    search_results = moly_search_results()

    checked_author = filter(lambda x: booksearch.check_for_author(x[0], ['Raymond E. Feist']), search_results)
    checked_title = filter(lambda x: booksearch.check_for_title(x[1], 'Ezusttovis'), search_results)

    # pprint.pprint(set(checked_author))
    pprint.pprint(set(checked_title))

    # pprint.pprint(search_results)

    # moly_book_details()
    print('Stop...')
