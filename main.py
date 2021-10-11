import pprint

import moly_hu.parser as parser
import moly_hu.parse_search as booksearch


def moly_book_details():
    with open('moly_hu/test/hu_series.html', 'r') as f:
        meta = parser.HtmlParser().extract_book_details(f.read())
        pprint.pprint(meta)


if __name__ == "__main__":
    print('asdf')
    with open('moly_hu/test/search_multiple_book.html', 'r') as f:
        pprint.pprint(booksearch.parse_search_results(f.read()))
