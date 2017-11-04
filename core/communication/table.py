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
from collections import UserDict


class Table(RedisObject):
    Redis_Type = "hash"

    def __init__(self, key):
        super(Table, self).__init__(key)

        # assert self.get_type() in (self.Redis_Type, RedisObject.Redis_Type), "Wrong Redis Object Type"

    def __getitem__(self, key):
        b_key = self.packb(key)
        b_item = self.redis.hget(self.key, b_key)
        if not b_item:
            raise KeyError(key)
        return self.unpackb(b_item)

    def __setitem__(self, key, value):
        b_key = self.packb(key)
        b_item = self.packb(value)
        self.redis.hset(self.key, b_key, b_item)

    def __len__(self):
        return self.redis.hlen(self.key)

    def __delitem__(self, key):
        b_key = self.packb(key)
        if not self.redis.hdel(self.key, b_key):
            raise KeyError(key)

    def __iter__(self):
        return iter(self.keys())

    def __contains__(self, key):
        b_key = self.packb(key)
        return self.redis.hexists(self.key, b_key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        return map(self.unpackb, self.redis.hkeys(self.key))

    def items(self):
        return map(lambda x: (self.unpackb(x[0]), self.unpackb(x[1])), self.redis.hgetall(self.key).items())

    def values(self):
        return map(self.unpackb, self.redis.hvals(self.key))

    def clear(self):
        self.redis.delete(self.key)

    def setdefault(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            self[key] = default
        return default
