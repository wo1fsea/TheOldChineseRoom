# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/5
Description:
    frame_capture.py
----------------------------------------------------------------------------"""

import mss
import time

from core.communication.queue import Queue
from core.config_reader import ConfigReader
from core.window_manager import WindowManager


class FrameCapture(object):
    def __init__(self):
        config = ConfigReader().get_config("frame_capture")
        self._mss = mss.mss()
        self._monitor = self._mss.monitors[0]

        self._queue = Queue(config["frame_cache_key"], config["frame_cache_length"])
        self._queue.clear()
        self._fps = config["fps"]
        self._frame_interval = 1. / self._fps
        self._last_capture_time = 0

    def capture_frame(self):
        capture_time = time.time()
        sct_img = self._mss.grab(self._monitor)
        self._queue.push(((sct_img.size.width, sct_img.size.height), sct_img.rgb).__repr__())
        interval = capture_time - self._last_capture_time
        self._last_capture_time = capture_time

        if self._frame_interval > interval:
            time.sleep(self._frame_interval - interval)

    def set_geometry(self, left, top, width, height):
        self._monitor = {"left": left, "top": top, "width": width, "height": height}


def start():
    wm = WindowManager()
    wg = wm.get_window_geometry("PokerHD")
    fc = FrameCapture()
    fc.set_geometry(wg["x"], wg["y"], wg["width"], wg["height"])
    while True:
        fc.capture_frame()

