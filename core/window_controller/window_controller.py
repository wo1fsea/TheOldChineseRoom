# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/4
Description:
    window_controller.py
----------------------------------------------------------------------------"""

import sys


class WindowController(object):
    def __init__(self):
        self.adapter = self._load_adapter()()

    def locate_window(self, name):
        return self.adapter.locate_window(name)

    def move_window(self, window_id, x, y):
        self.adapter.move_window(window_id, x, y)

    def resize_window(self, window_id, width, height):
        self.adapter.resize_window(window_id, width, height)

    def focus_window(self, window_id):
        self.adapter.focus_window(window_id)

    def is_window_focused(self, window_id):
        return self.adapter.is_window_focused(window_id)

    def get_focused_window_name(self):
        return self.adapter.get_focused_window_name()

    def get_window_geometry(self, window_id):
        return self.adapter.get_window_geometry(window_id)

    def _load_adapter(self):
        if sys.platform == "darwin":
            from .window_controller_darwin import WindowControllerDarwin
            return WindowControllerDarwin
        elif sys.platform == "win32":
            from .window_controller_win32 import WindowControllerWin32
            return WindowControllerWin32
        elif sys.platform in ["linux", "linux2"]:
            raise NotImplementedError()
        else:
            raise NotImplementedError()
