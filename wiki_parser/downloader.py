# -*- coding: utf-8 -*-


import requests
from requests import HTTPError
from requests.exceptions import RequestException


class PageNotFound(Exception):
    pass


class BadInternetConnection(Exception):
    pass


class Downloader(object):

    def __init__(self):
        self.session = requests.session()

    def get(self, url):
        url = u'https://uk.wikipedia.org/wiki/{}'.format(url)
        try:
            request = self.session.get(url, timeout=3)
            request.raise_for_status()
            return request.content
        except HTTPError:
            raise PageNotFound()
        except RequestException:
            raise BadInternetConnection()
