# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/5
Description:
    window_manager_darwin.py
----------------------------------------------------------------------------"""

from .window_manager import WindowManager
import applescript


class WindowManagerDarwin(WindowManager):
    def __init__(self):
        pass

    def locate_window(self, name):
        return name

    def move_window(self, window_id, x, y):
        applescript.AppleScript(f'''
            tell application "System Events" to tell window 1 of process "{window_id}"
                set position to { {x}, {y} }
            end tell
        ''').run()

    def resize_window(self, window_id, width, height):
        applescript.AppleScript(f'''
            tell application "System Events" to tell window 1 of process "{window_id}"
                set size to { {width}, {height} }
            end tell
        ''').run()

    def focus_window(self, window_id):
        applescript.AppleScript(f'''
            tell application "System Events" to tell process "{window_id}"
                set frontmost to true
            end tell
        ''').run()

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

        window_geometry = applescript.AppleScript(f'''
            tell application "System Events" to tell process "{window_id}"
                return get size of window 1
            end tell
        ''').run()

        geometry["width"] = int(window_geometry[0])
        geometry["height"] = int(window_geometry[1])

        window_information = applescript.AppleScript(f'''
            tell application "System Events" to tell window 1 of process "{window_id}"
                return get position
            end tell
        ''').run()

        geometry["x"] = int(window_information[0])
        geometry["y"] = int(window_information[1])

        return geometry
