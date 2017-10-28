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

from .redis_object import RedisObject


class Table(RedisObject):
    Redis_Type = "hash"

    def __init__(self, key):
        super(Table, self).__init__(key)

        assert self.get_type() in (self.Redis_Type, RedisObject.Redis_Type), "Wrong Redis Object Type"

    def __getitem__(self, key):
        b_key = self.packb(key)
        b_item = self.db_connection.hget(self.key, b_key)
        if not b_item:
            raise KeyError(key)
        return self.unpackb(b_item)

    def __setitem__(self, key, value):
        b_key = self.packb(key)
        b_item = self.packb(value)
        self.db_connection.hset(self.key, b_key, b_item)

    def __len__(self):
        return self.db_connection.hlen(self.key)

    def __delitem__(self, key):
        b_key = self.packb(key)
        if not self.db_connection.hdel(self.key, b_key):
            raise KeyError(key)

    def __iter__(self):
        return iter(self.keys())

    def __contains__(self, key):
        b_key = self.packb(key)
        return self.db_connection.hexists(self.key, b_key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        return map(self.unpackb, self.db_connection.hkeys(self.key))

    def items(self):
        return map(lambda k, v: (k, self.unpackb(v)), self.db_connection.hgetall().items())

    def values(self):
        return map(self.unpackb, self.db_connection.hvals(self.key))

    def clear(self):
        self.db_connection.delete(self.key)
