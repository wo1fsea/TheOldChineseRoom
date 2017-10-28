# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/29
Description:
    redis_object.py
----------------------------------------------------------------------------"""

import msgpack

from . import db_connection


class RedisObject(object):

    Redis_Type = "none"

    def __init__(self, key):
        self._key = key
        self.redis = db_connection.get_redis()

    def get_type(self):
        return self.redis.type(self._key).decode()

    def set_expire(self, milliseconds):
        self.redis.pexpire(self._key, milliseconds)

    @property
    def key(self):
        return self._key

    @staticmethod
    def packb(obj):
        return msgpack.packb(obj)

    @staticmethod
    def unpackb(packed):
        return msgpack.unpackb(packed, encoding='utf-8')
