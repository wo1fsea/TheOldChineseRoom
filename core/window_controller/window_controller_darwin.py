# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/5
Description:
    window_controller_darwin.py
----------------------------------------------------------------------------"""

from .window_controller import WindowController
import applescript


class WindowControllerDarwin(WindowController):
    def __init__(self):
        pass

    def locate_window(self, name):
        return name

    def move_window(self, window_id, x, y):
        applescript.AppleScript('''
            tell application "System Events" to tell window 1 of process "{window_id}"
                set position to {{ {x}, {y} }}
            end tell
        '''.format(window_id=window_id, x=x, y=y)).run()

    def resize_window(self, window_id, width, height):
        applescript.AppleScript('''
            tell application "System Events" to tell window 1 of process "{window_id}"
                set size to {{ {width}, {height} }}
            end tell
        '''.format(window_id=window_id, width=width, height=height)).run()

    def focus_window(self, window_id):
        applescript.AppleScript('''
            tell application "System Events" to tell process "{window_id}"
                set frontmost to true
            end tell
        '''.format(window_id=window_id)).run()

    def is_window_focused(self, window_id):
        return self.get_focused_window_name() == window_id

    def get_focused_window_name(self):
        focused_window_id = applescript.AppleScript('''
            tell application "System Events"
                return title of first application process whose frontmost is true
            end tell
        ''').run()

        return focused_window_id

    def get_window_geometry(self, window_id):
        geometry = dict()

        window_geometry = applescript.AppleScript('''
            tell application "System Events" to tell process "{window_id}"
                return get size of window 1
            end tell
        '''.format(window_id=window_id)).run()

        geometry["width"] = int(window_geometry[0])
        geometry["height"] = int(window_geometry[1])

        window_information = applescript.AppleScript('''
            tell application "System Events" to tell window 1 of process "{window_id}"
                return get position
            end tell
        '''.format(window_id=window_id)).run()

        geometry["x"] = int(window_information[0])
        geometry["y"] = int(window_information[1])

        return geometry
