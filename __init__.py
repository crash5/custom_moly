#!/usr/bin/env python


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

    SEARCH_URL = 'https://moly.hu/kereses?utf8=%E2%9C%93&q='
    BASE_URL = 'https://moly.hu/'

    def identify(self, log, result_queue, abort, title=None, authors=None, identifiers={}, timeout=30):
        log.info('veluna begin')


        query = self.SEARCH_URL + f'{authors[0]}  {title}'
        log.info(query)


        br = browser()
        response = br.open(query)
        raw = response.read().strip()
        raw = raw.decode('utf-8', errors='replace')
        content = clean_ascii_chars(raw)

        search_result = list(parse_search.parse_search_results(content))
        log.info(search_result)


        bookurl = self.BASE_URL + search_result[0][2]
        resp2 = br.open_novisit(bookurl)
        raw2 = resp2.read().strip()
        # raw2 = raw.decode('utf-8', errors='replace')
        content2 = clean_ascii_chars(raw2)
        parser = parse_book.HtmlParser()
        book_res = parser.extract_book_details(content2)
        log.info(book_res)

        meta = Metadata(book_res['title'], book_res['authors'])
        result_queue.put(meta)

        # books = [
        #     Metadata('aaaaaaaaaaaaaaa', ['author']),
        #     # Metadata('sdfsdf sdfsdafsda fsd', ['another autor']),
        #     # Metadata('sdfdsfasdf dsfsd fsdf sdaf', ['dfsdfsd fads fgrfggfh d fg']),
        #     # Metadata('title2', ['author2'])
        # ]

        # for book in books:
        #     book.source_relevance = 0
        #     result_queue.put(book)

        log.info('veluna end')
        return None
