# -*- coding: utf-8 -*-

import gevent
import logging

import db

from downloader import Downloader, PageNotFound, BadInternetConnection


class Task(object):

    def __init__(self, page_manager, references_manager,
                 task_queue, worker_count, parser, downloader):
        self.page_manager = page_manager
        self.references_manager = references_manager
        self.task_queue = task_queue
        self.worker_count = worker_count
        self.parser = parser
        self.downloader = downloader

    def run(self):
        greenlets = [gevent.spawn(self.task_queue.fill_queue)]
        greenlets.extend(
            [
                 gevent.spawn(self.worker)
                 for i in range(self.worker_count)
            ]
        )
        gevent.joinall(greenlets)

    def worker(self):
        downloader = Downloader()

        while not self.task_queue._is_stopped or not self.task_queue.empty():
            try:
                page_id, page_url = self.task_queue.get()
                logging.info(u'get id={}, url={}'.format(page_id, page_url))

                data = downloader.get(url=page_url)
                with open('../downloaded_pages/{}.html'.format(page_id), 'w') as file:
                    file.write(data)

                page_urls = self.parser.parse(data=data)
                page_urls = self.processing_page_urls(page_urls=page_urls)

                self.references_manager.insert_references(
                    current_page_id=page_id,
                    references_page_ids=page_urls.values())

                self.page_manager.mark_as(
                    page_ids=[page_id], status=db.STATUS_PROCESSED)
                logging.info(u'done id={}, url={}'.format(page_id, page_url))
            except BadInternetConnection as e:
                logging.error(repr(e))
                self.page_manager.mark_as(
                    page_ids=[page_id], status=db.STATUS_BAD_INTERNET_CONNECTION)
                gevent.sleep(20)
            except PageNotFound as e:
                logging.error(repr(e))
                self.page_manager.mark_as(
                    page_ids=[page_id], status=db.STATUS_NOT_FOUND)
            except Exception as e:
                print type(e)
                logging.error(repr(e), exc_info=True)
                self.page_manager.mark_as(
                    page_ids=[page_id], status=db.STATUS_UNKNOWN_ERROR)

    def processing_page_urls(self, page_urls):
        page_urls = {
            url: None
            for url in page_urls
        }

        page_urls_existed = self.page_manager.get_existed(
            page_urls=page_urls.keys())
        for url in page_urls_existed:
            page_urls[url.page_url] = url.page_id

        page_urls_new = [
            page_url
            for page_url, page_id in page_urls.iteritems()
            if not page_id
        ]
        self.page_manager.insert_urls(page_urls_new)

        page_urls_new = self.page_manager.get_existed(page_urls=page_urls_new)
        for url in page_urls_new:
            page_urls[url.page_url] = url.page_id

        return page_urls
