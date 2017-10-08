# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/6
Description:
    table.py
----------------------------------------------------------------------------"""

import msgpack

from .db_connection import DBConnection


class Table(object):
    def __init__(self, key):
        self.key = key
        self.db_connection = DBConnection().redis

    def __getitem__(self, key):
        b_item = self.db_connection.hget(self.key, key)
        item = msgpack.unpackb(b_item) if b_item else b_item
        return item

    def __setitem__(self, key, value):
        b_item = msgpack.packb(value)
        self.db_connection.hset(self.key, key, b_item)

    def clear(self):
        self.db_connection.delete(self.key)