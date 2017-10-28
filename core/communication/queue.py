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

from .redis_object import RedisObject

QUEUE_MAX_LENGTH = -1


class Queue(RedisObject):
    def __init__(self, key, max_len=QUEUE_MAX_LENGTH):
        super(Queue, self).__init__(key)
        self.max_len = max_len

    def put(self, item):
        b_item = self.packb(item)
        self.redis.lpush(self.key, b_item)
        if self.max_len > 0:
            self.redis.ltrim(self.key, 0, self.max_len)

    def get(self):
        b_item = self.redis.rpop(self.key)
        item = self.unpackb(b_item) if b_item else b_item
        return item

    def bget(self):
        b_item = self.redis.brpop(self.key)[1]
        item = self.unpackb(b_item) if b_item else b_item
        return item

    def clear(self):
        self.redis.delete(self.key)
