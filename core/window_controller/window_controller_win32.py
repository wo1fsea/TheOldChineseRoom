# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/4
Description:
    window_controller_win32.py
----------------------------------------------------------------------------"""

from .window_controller import WindowController
import win32gui


class WindowControllerWin32(WindowController):
    def __init__(self):
        pass

    def locate_window(self, name):
        return win32gui.FindWindow(None, name)

    def move_window(self, window_id, x, y):
        x0, y0, x1, y1 = win32gui.GetWindowRect(window_id)
        win32gui.MoveWindow(window_id, x, y, x1 - x0, y1 - y0, True)

    def resize_window(self, window_id, width, height):
        x0, y0, x1, y1 = win32gui.GetWindowRect(window_id)
        win32gui.MoveWindow(window_id, x0, y0, width, height, True)

    def focus_window(self, window_id):
        win32gui.SetForegroundWindow(window_id)

    def is_window_focused(self, window_id):
        focused_window_id = win32gui.GetForegroundWindow()
        return focused_window_id == window_id

    def get_focused_window_name(self):
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())

    def get_window_geometry(self, window_id):
        geometry = dict()

        x, y, width, height = win32gui.GetClientRect(window_id)

        geometry["width"] = width
        geometry["height"] = height

        x0, y0, x1, y1 = win32gui.GetWindowRect(window_id)

        border_width = ((x1 - x0 - width) // 2)

        geometry["x"] = x0 + border_width
        geometry["y"] = y0 + (y1 - y0 - height - border_width)

        return geometry
