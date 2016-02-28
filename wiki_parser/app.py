#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal

import db
import configs

from task import Task
from queue import QueueTask
from downloader import Downloader
from parser import Parser


class App(object):

    def __init__(self):
        self.db = configs.create_engine()
        self.page_manager = db.PageManager(db=self.db)
        self.references_manager = db.ReferencesManager(db=self.db)

        self.worker_count = configs.WORKER_COUNT

        self.downloader = Downloader()
        self.parser = Parser()

        self.task_queue = QueueTask(
            page_manager=self.page_manager,
            size=4 * self.worker_count)

        self.task = Task(
            page_manager=self.page_manager,
            references_manager=self.references_manager,
            task_queue=self.task_queue,
            worker_count=self.worker_count,
            parser=self.parser,
            downloader=self.downloader
        )

    def run(self):
        signal.signal(
            signal.SIGINT, (lambda signum, frame: self.task_queue.stop()))

        self.task.run()
