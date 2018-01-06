# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/7
Description:
    launcher.py
----------------------------------------------------------------------------"""

import sys

from grabber import grabber
from monitor import monitor
from redis_docker import redis_docker

modules = {
    "grabber": grabber.start,
    "monitor": monitor.start,
    "redis_docker": redis_docker.start,
}


def main():
    module_name = sys.argv[1]
    assert module_name in modules, "module %s not exists" % module_name
    modules[module_name]()


if __name__ == '__main__':
    main()
