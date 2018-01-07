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
import struct
from PIL import Image

from ..communication.queue import Queue
from ..communication.table import Table
from ..communication.redis_object import NoPacker
from ..config_reader import ConfigReader


class FrameReader(object):
    def __init__(self):
        super(FrameReader, self).__init__()
        config = ConfigReader().get_config("frame_grabber")

        self._size = Table(config["frame_size_key"])

        self._queue = Queue(config["frame_cache_key"], packer=NoPacker, max_len=config["frame_cache_length"])

        self._fps = config["fps"]
        self._frame_interval = 1. / self._fps
        self._last_frame_size = 0

    def read_frame(self):
        data = self._queue.get()
        if data:
            data = zlib.decompress(data)
            size = struct.unpack("II", data[:8])
            frame = Image.frombytes('RGB', size, data[8:])
        else:
            frame = None

        return frame

