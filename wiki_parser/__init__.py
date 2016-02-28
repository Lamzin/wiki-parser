# -*- coding: utf-8 -*-


from app import App


import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='wiki_ua.log',
                    filemode='w')
