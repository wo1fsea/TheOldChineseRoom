# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/1/13
Description:
    grabber_watcher_test.py
----------------------------------------------------------------------------"""

from core.watcher import WatcherClient

wc = WatcherClient("grabber")
print(wc.get_commands())
print(wc.run_command("p", 100))