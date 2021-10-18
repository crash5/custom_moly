#!/usr/bin/env python

import concurrent.futures

from calibre.ebooks.metadata.book.base import Metadata
from calibre import browser
from calibre.ebooks.metadata.sources.base import Source
from calibre.utils.cleantext import clean_ascii_chars

import calibre_plugins.veluna_metadata.moly_hu.parse_search as parse_search
import calibre_plugins.veluna_metadata.moly_hu.parser as parse_book


__license__   = 'GPL v3'
__copyright__ = '2011, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'


class VelunaMetadata(Source):
    name = 'Veluna metadat source'
    version = (1, 0, 0)
    minimum_calibre_version = (2, 80, 0)
    description = _('dl metadata')

    capabilities = frozenset(['identify'])

    def identify(self, log, result_queue, abort, title=None, authors=None, identifiers={}, timeout=30):
        base_url = 'https://moly.hu/'

        search_param = f'{authors[0]}  {title}'
        books = get_for_search(base_url, f'kereses?utf8=%E2%9C%93&q={search_param}')

        for book in books:
            result_queue.put(book)

        return None


def get_url_content(url):
    br = browser()
    response = br.open(url)
    raw = response.read().strip()
    raw = raw.decode('utf-8', errors='replace')
    return clean_ascii_chars(raw)


def get_book_meta(url):
    book_url = url
    book_page_source = get_url_content(book_url)
    book_data = parse_book.HtmlParser().extract_book_details(book_page_source)
    return Metadata(book_data['title'], book_data['authors'])


def get_for_search(base_url, search_param):
    search_url = base_url + search_param
    search_page_source = get_url_content(search_url)
    search_result = parse_search.parse_search_results(search_page_source)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_book_meta, base_url + result[2]): result for result in search_result}
        for future in concurrent.futures.as_completed(futures):
            # result = futures[future]
            try:
                book_meta = future.result()
                yield book_meta
            except Exception as exc:
                print(f'generated an exception: {exc}')
            # else:
            #     print(f'{id} - {name}: done')
