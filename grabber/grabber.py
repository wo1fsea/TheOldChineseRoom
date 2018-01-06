# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/1/6
Description:
    grabber.py
----------------------------------------------------------------------------"""

from core.window_controller import WindowController
from core.frame_grabber import FrameGrabber

import time

def start():
    wm = WindowController()
    fc = FrameGrabber()
    # win_name = "电影和电视"
    win_name = wm.get_focused_window_name()
    win = wm.locate_window(win_name)
    wg = wm.get_window_geometry(win)
    fc.set_geometry(wg["x"], wg["y"], wg["width"], wg["height"])

    last_check = time.time()

    while True:
        if time.time() - last_check > 1:
            wg = wm.get_window_geometry(win)
            fc.set_geometry(wg["x"], wg["y"], wg["width"], wg["height"])
            last_check = time.time()

        fc.grab_frame()
