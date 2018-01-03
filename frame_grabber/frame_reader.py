# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/1/4
Description:
    frame_reader.py
----------------------------------------------------------------------------"""

import zlib
from PIL import Image

from core.communication.queue import Queue
from core.communication.table import Table
from core.config_reader import ConfigReader


class FrameReader(object):
    def __init__(self):
        super(FrameReader, self).__init__()
        config = ConfigReader().get_config("frame_grabber")

        self._size = Table(config["frame_size_key"])

        self._queue = Queue(config["frame_cache_key"], config["frame_cache_length"], pack_item=False)

        self._fps = config["fps"]
        self._frame_interval = 1. / self._fps
        self._last_frame_size = 0

    def read_frame(self):
        size = self._size["width"], self._size["height"]
        data = self._queue.get()
        if data:
            frame = Image.frombytes('RGB', size, zlib.decompress(data))
        else:
            frame = None

        return frame

