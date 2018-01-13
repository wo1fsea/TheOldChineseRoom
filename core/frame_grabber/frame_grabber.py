# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/5
Description:
    frame_grabber.py
----------------------------------------------------------------------------"""

import mss
import time
import zlib
import struct
from ..communication.collections.queue import Queue
from ..communication.collections.dict import Dict
from ..communication.collections.redis_object import NoPacker
from ..config_reader import ConfigReader


class FrameGrabber(object):
    def __init__(self):
        super(FrameGrabber, self).__init__()

        config = ConfigReader().get_config("frame_grabber")
        self._mss = mss.mss()
        self._monitor = self._mss.monitors[1]

        self._size = Dict(config["frame_size_key"])
        self._update_frame_size()

        self._queue = Queue(config["frame_cache_key"], packer=NoPacker, max_len=config["frame_cache_length"])
        self._queue.clear()

        self._fps = config["fps"]
        self._frame_interval = 1. / self._fps
        self._last_grab_time = 0

    def _update_frame_size(self):
        self._size["width"] = self._monitor["width"]
        self._size["height"] = self._monitor["height"]

    def grab_frame(self):
        grab_time = time.time()
        sct_img = self._mss.grab(self._monitor)
        self._queue.put(zlib.compress(struct.pack("II", sct_img.width, sct_img.height) + sct_img.rgb, 3))
        interval = grab_time - self._last_grab_time
        self._last_grab_time = grab_time
        if self._frame_interval > interval:
            time.sleep(self._frame_interval - interval)

    def set_geometry(self, left, top, width, height):
        self._queue.clear()
        self._monitor = {"left": left, "top": top, "width": width, "height": height}
        self._update_frame_size()


