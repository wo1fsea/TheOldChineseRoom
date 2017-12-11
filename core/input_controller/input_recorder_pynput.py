# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/12/3
Description:
    input_recorder_pyuserinput.py
----------------------------------------------------------------------------"""

import time
from threading import Thread

from pynput import keyboard
from pynput import mouse

from core.input_controller.input_recorder import InputRecorder
from core.input_controller.input_controller_pynput import PYNPUT_KEYBOARD_MAP, PYNPUT_MOUSE_MAP

PYNPUT_KEYBOARD_REVERSE_MAP = {v: k for k, v in PYNPUT_KEYBOARD_MAP.items()}
PYNPUT_MOUSE_MAP = {v: k for k, v in PYNPUT_MOUSE_MAP.items()}


class InputRecorderPynput(InputRecorder):
    def __init__(self, record_mouse_moving):
        self._record_mouse_moving = record_mouse_moving
        self._is_recording = False
        self._mouse_listener = None
        self._mouse_record_thread = None
        self._keyboard_listener = None
        self._keyboard_record_thread = None

    def on_click(self, x, y, button, pressed):
        print(x, y, button, pressed)

    def on_move(self, x, y):
        print(x, y)

    def on_scroll(self, x, y, dx, dy):
        print(x, y, dx, dy)

    def on_press(self, key):
        print(key)

    def on_release(self, key):
        print(key)

    def start_record(self):
        assert self._is_recording is False, "input recorder is already recording."
        self._is_recording = True

        self._mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        self._keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

        self._mouse_listener.start()
        self._keyboard_listener.start()

    def stop_record(self):
        if not self._is_recording:
            return

        self._is_recording = False

        self._mouse_listener.join()
        self._keyboard_listener.join()

    def start_replay(self):
        pass

    def stop_replay(self):
        pass
