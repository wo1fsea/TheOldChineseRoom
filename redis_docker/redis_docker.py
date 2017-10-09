# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/9
Description:
    redis_docker.py
----------------------------------------------------------------------------"""

import docker


def start():
    client = docker.from_env()
    # client.containers.
    redis_docker = client.containers.get("redis")
    if not redis_docker:
        client.containers.run("redis", name="redis", ports={"6379/tcp": 6379}, detach=True)
    else:
        if redis_docker.status != "running":
            redis_docker.start()

