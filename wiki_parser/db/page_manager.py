# -*- coding: utf-8 -*-


STATUS_PROCESSED = u'processed'
STATUS_UNPROCESSED = u'unprocessed'
STATUS_IN_PROCESSING = u'in_processing'
STATUS_NOT_FOUND = u'page_not_found'
STATUS_BAD_INTERNET_CONNECTION = u'bad_internet_connection'
STATUS_UNKNOWN_ERROR = u'unknown_error'


class PageManager(object):

    def __init__(self, db):
        self.db = db

    def get_new_pages(self, count):
        query = u"""
            SELECT page_id, page_url
            FROM pages
            WHERE status = '{status}'
            LIMIT {count}
            FOR UPDATE
        """.format(status=STATUS_UNPROCESSED, count=count)

        with self.db.begin() as db_transaction:
            rows = db_transaction.execute(query).fetchall()

            page_ids = [row.page_id for row in rows]
            if page_ids:
                self._update_status(
                    db_transaction, page_ids, STATUS_IN_PROCESSING)

        return rows or []

    def get_existed(self, page_urls):
        if not page_urls:
            return []

        values = u','.join([u"'{}'".format(url) for url in page_urls])

        query = u"""
            SELECT page_id, page_url
            FROM pages
            WHERE page_url IN ({values})
        """.format(values=values)
        with self.db.connect() as db_connect:
            rows = db_connect.execute(query).fetchall()

        return rows or []

    def insert_urls(self, page_urls):
        if not page_urls:
            return

        values = u', '.join([
            u"('{}', '{}')".format(url, STATUS_UNPROCESSED)
            for url in page_urls
        ])

        query = u"""
            INSERT IGNORE INTO pages(page_url, status)
            VALUES {values}
        """.format(values=values)

        with self.db.connect() as db_connect:
            db_connect.execute(query)

    @staticmethod
    def _update_status(connection, page_ids, status):
        if not page_ids:
            return
        query = u"""
            UPDATE pages
               SET status = '{status}'
             WHERE page_id IN ({values})
        """.format(status=status, values=u", ".join(map(str, page_ids)))

        connection.execute(query)

    def mark_as(self, page_ids, status):
        with self.db.connect() as db_connection:
            self._update_status(db_connection, page_ids, status)
