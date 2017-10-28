# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/5
Description:
    queue.py
----------------------------------------------------------------------------"""

import msgpack

from .db_connection import DBConnection

QUEUE_MAX_LENGTH = -1


class Queue(object):
    def __init__(self, key, max_len=QUEUE_MAX_LENGTH):
        self.key = key
        self.max_len = max_len
        self.db_connection = DBConnection().redis

    def put(self, item):
        b_item = msgpack.packb(item)
        self.db_connection.lpush(self.key, b_item)
        if self.max_len > 0:
            self.db_connection.ltrim(self.key, 0, self.max_len)

    def get(self):
        b_item = self.db_connection.rpop(self.key)
        item = msgpack.unpackb(b_item, encoding='utf-8') if b_item else b_item
        return item

    def bget(self):
        b_item = self.db_connection.brpop(self.key)[1]
        item = msgpack.unpackb(b_item, encoding='utf-8') if b_item else b_item
        return item

    def clear(self):
        self.db_connection.delete(self.key)
