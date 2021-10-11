from lxml.html import fromstring
import re


class HtmlParser:
    def extract_book_details(self, content):
        root = fromstring(content)
        metadata = {
            'title': self.parse_title(root),
            'authors': self.parse_authors(root),
            'publisher': self.parse_publisher(root),
            'published': self.parse_published_date(root),
            'series': self.parse_series(root),
            'tags': self.parse_tags(root),
            'rating': self.parse_rating(root),
            'comments': self.parse_comments(root),
            'languages': self.parse_languages(self.parse_tags(root)),
            'covers': self.parse_covers(root),
            'identifiers': {
                'isbn': self.parse_isbn(root)
            }
        }
        return metadata


    @staticmethod
    def parse_covers(root):
        book_covers = root.xpath('(//*[@class="coverbox"]//a/@href)')
        if book_covers:
            return [cover_url for cover_url in book_covers]


    @staticmethod
    def parse_languages(tags):
        def _translateLanguageToCode(displayLang):
            displayLang = displayLang.lower().strip() if displayLang else None
            langTbl = { None: 'und', 
                        u'angol nyelv\u0171': 'en',
                        u'n\xe9met nyelv\u0171': 'de',
                        u'francia nyelv\u0171': 'fr',
                        u'olasz nyelv\u0171': 'it', 
                        u'spanyol nyelv\u0171': 'es',
                        u'orosz nyelv\u0171': 'ru',
                        u't\xf6r\xf6k nyelv\u0171': 'tr',
                        u'g\xf6r\xf6g nyelv\u0171': 'gr',
                        u'k\xednai nyelv\u0171': 'cn',
                        u'jap\xe1n nyelv\u0171': 'jp' }
            return langTbl.get(displayLang, None)
        langs = []
        for tag in tags:
            langId = _translateLanguageToCode(tag)
            if langId is not None:
                langs.append(langId)
        if not langs:
            return ['hu']
        return langs


    @staticmethod
    def parse_isbn(root):
        isbn = None
        isbn_node = root.xpath('//*[@id="content"]//*[@class="items"]/div/div[2]/text()')
        for isbn_value in isbn_node:
            m = re.search(r'(\d{13}|\d{10})', isbn_value)
            if m:
                isbn = m.group(1)
                break
        return isbn


    @staticmethod
    def parse_published_date(root):
        pub_year = None
        publication_node = root.xpath('//*[@id="content"]//*[@class="items"]/div/div[1]/text()')
        for publication_value in publication_node:
            m = re.search(r'(\d{4})', publication_value)
            if m:
                pub_year = m.group(1)
                break
        return pub_year


    @staticmethod
    def parse_title(root):
        title_node = root.xpath('//*[@id="content"]//*[@class="fn"]/text()')
        if not title_node:
            title_node = root.xpath('//*[@id="content"]//*[@class="item"]/text()')
        if title_node:
            #Cimből a ZWJ (zero-width joiner = nulla szélességű szóköz) karakter (\u200b) eltávolítása
            return title_node[0].strip().replace('\u200b', '')


    @staticmethod
    def parse_authors(root):
        author_nodes = root.xpath('//*[@id="content"]//div[@class="authors"]/a/text()')
        if author_nodes:
            return [str(author) for author in author_nodes]


    @staticmethod
    def parse_publisher(root):
        publisher_node = root.xpath('//*[@id="content"]//*[@class="items"]/div/div[1]/a/text()')
        if publisher_node:
            return publisher_node[0]


    @staticmethod
    def parse_rating(root):
        rating_node = root.xpath('//*[@id="content"]//*[@class="rating"]//*[@class="like_count"]/text()')
        if rating_node:
            return round(float(rating_node[0].strip('%').strip())*0.05)


    @staticmethod
    def parse_series(root):
        series_node = root.xpath('//*[@id="content"]//*[@class="action"]/text()')
        if not series_node:
            return None
        return series_node[0].strip('().').rsplit(' ', 1)


    @staticmethod
    def parse_tags(root):
        tags_node = root.xpath('//*[@id="tags"]//*[@class="hover_link"]/text()')
        tags_node = [str(text) for text in tags_node if text.strip()]
        if tags_node:
            return tags_node


    @staticmethod
    def parse_comments(root):
        description_node = root.xpath('//*[@id="content"]//*[@class="text" and @id="full_description"]/p/text()')
        if not description_node:
            description_node = root.xpath('//*[@id="content"]//*[@class="text"]/p/text()')
        if description_node:
            #Megjegyzésből dupla, vagy space-t tartalmazó dupla soremelések eltávolítása
            join_desc_node = '\n'.join(description_node)
            if join_desc_node.count('\n\n') > 0:
                join_desc_node = join_desc_node.replace('\n\n', '\n')
            if join_desc_node.count('\n \n') > 0:
                join_desc_node = join_desc_node.replace('\n \n', '\n')
            #Megjegyzésből a "Vigyázat! Cselekményleírást tartalmaz." szövegrész eltávolítása
            join_desc_node = join_desc_node.replace('Vigyázat! Cselekményleírást tartalmaz.\n', '')
            #Eredeti parancs: return '\n'.join(description_node)
            return join_desc_node

