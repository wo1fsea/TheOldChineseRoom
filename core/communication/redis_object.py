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

from .db_connection import DBConnection


class RedisObject(object):

    Redis_Type = "none"

    def __init__(self, key):
        self._key = key
        self.db_connection = DBConnection().redis

    def get_type(self):
        return self.db_connection.type(self._key).decode()

    def set_expire(self, milliseconds):
        self.db_connection.pexpire(self._key, milliseconds)

    @property
    def key(self):
        return self._key

    @staticmethod
    def packb(obj):
        return msgpack.packb(obj)

    @staticmethod
    def unpackb(packed):
        return msgpack.unpackb(packed, encoding='utf-8')
