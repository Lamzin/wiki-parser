# -*- coding: utf-8 -*-


from lxml import html


class Parser(object):

    def __init__(self):
        self.parser = html.HTMLParser(encoding='utf-8')
        self.selector = u'//div[@class="mw-body-content"]' \
                        u'//a[starts-with(@href, "/wiki")]/@title'

    def parse(self, data):
        document = html.document_fromstring(data, parser=self.parser)
        return [
            result
            for result in document.xpath(self.selector)
            if '\'' not in result
        ]
