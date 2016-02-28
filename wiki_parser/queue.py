# -*- coding: utf-8 -*-

import gevent
import logging

from gevent.queue import Queue


class QueueTask(Queue):

    def __init__(self, page_manager, size):
        super(self.__class__, self).__init__(maxsize=size)
        self.page_manager = page_manager
        self._is_stopped = False

    def fill_queue(self):
        while not self._is_stopped:
            try:
                logging.info('Try to get jobs!')
                rows = self.page_manager.get_new_pages(self.maxsize)
                if rows:
                    for row in rows:
                        self.put((row.page_id, unicode(row.page_url)))
                else:
                    gevent.sleep(60)

            except Exception as e:
                logging.error(e, exc_info=True)
        logging.info("Queue is stopped")

    def stop(self):
        self._is_stopped = True
