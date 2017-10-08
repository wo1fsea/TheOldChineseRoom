# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/5
Description:
    db_connection.py
----------------------------------------------------------------------------"""

import redis

from utils.singleton import Singleton

from ..config_reader import ConfigReader


class DBConnection(Singleton):
    def __init__(self):
        config_reader = ConfigReader()
        redis_config = config_reader.get_config("redis")
        assert redis_config, "redis config not exists."
        self._redis = redis.StrictRedis(**redis_config)

    @property
    def redis(self):
        return self._redis
