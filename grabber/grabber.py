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
from core.watcher import Watcher

import time

is_running = True


def cmd_print(i):
    print(i)
    return int(i) + 1


def cmd_exit():
    global is_running
    is_running = False


def start():
    wm = WindowController()
    fc = FrameGrabber()
    watcher = Watcher("grabber")
    watcher.register_commands({"print": cmd_print, "exit": cmd_exit})
    watcher.start_watcher_command_service()

    # win_name = "电影和电视"
    win_name = wm.get_focused_window_name()
    win = wm.locate_window(win_name)
    wg = wm.get_window_geometry(win)
    fc.set_geometry(wg["x"], wg["y"], wg["width"], wg["height"])

    last_check = time.time()

    global is_running
    is_running = True
    while is_running:
        if time.time() - last_check > 1:
            wg = wm.get_window_geometry(win)
            fc.set_geometry(wg["x"], wg["y"], wg["width"], wg["height"])
            last_check = time.time()
            watcher.set_status(wg)

        fc.grab_frame()

    watcher.stop_watcher_command_service()
