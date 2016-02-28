# -*- coding: utf-8 -*-


class ReferencesManager(object):

    def __init__(self, db):
        self.db = db

    def insert_references(self, current_page_id, references_page_ids):
        if not references_page_ids:
            return

        values = u", ".join(
            [
                u"({}, {})".format(current_page_id, references_page_id)
                for references_page_id in references_page_ids
                if references_page_id
            ]
        )
        query = u"""
            INSERT INTO `references`(root, child)
            VALUES {values}
        """.format(values=values)

        with self.db.connect() as db_connection:
            db_connection.execute(query)
