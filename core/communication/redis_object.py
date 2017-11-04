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
import time
from . import db_connection

_delta_time = None


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
    def exists(self):
        return self.redis.exists(self._key)

    @property
    def time(self):
        global _delta_time
        if _delta_time is None:
            local_time = time.time()
            redis_time = float("%d.%d" % self.redis.time())
            _delta_time = redis_time - local_time
        return _delta_time + time.time()

    @property
    def key(self):
        return self._key

    @staticmethod
    def packb(obj):
        return msgpack.packb(obj)

    @staticmethod
    def unpackb(packed):
        return msgpack.unpackb(packed, encoding='utf-8')
