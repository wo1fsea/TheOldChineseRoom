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

from pynput import keyboard
from pynput import mouse

from .keys import Keyboard, Mouse, CHARACTER_KEY_MAP
from core.input_controller.input_recorder import InputRecorder, Logger
from core.input_controller.input_controller_pynput import KEYBOARD_MAP, MOUSE_MAP

KEYBOARD_REVERSE_MAP = {v: k for k, v in KEYBOARD_MAP.items()}
KEYBOARD_REVERSE_MAP.update({k: k for k in CHARACTER_KEY_MAP.keys()})
print(KEYBOARD_REVERSE_MAP.get(keyboard))
MOUSE_REVERSE_MAP = {v: k for k, v in MOUSE_MAP.items()}


class InputRecorderPynput(InputRecorder):
    def __init__(self, record_mouse_moving):
        self._record_mouse_moving = record_mouse_moving
        self._is_recording = False
        self._mouse_listener = None
        self._mouse_record_thread = None
        self._keyboard_listener = None
        self._keyboard_record_thread = None

        self._logger = Logger()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self._logger.log_mouse_press(MOUSE_REVERSE_MAP.get(button, Mouse.BUTTON_UNKNOWN), (x, y))
        else:
            self._logger.log_mouse_release(MOUSE_REVERSE_MAP.get(button, Mouse.BUTTON_UNKNOWN), (x, y))

    def on_move(self, x, y):
        self._logger.log_mouse_move_to((x, y))

    def on_scroll(self, x, y, dx, dy):
        self._logger.log_mouse_scroll(dy, (x, y))

    def on_press(self, key):
        self._logger.log_key_press(KEYBOARD_REVERSE_MAP.get(key.char if key.char is not None else key, Keyboard.KEY_UNKNOWN))

    def on_release(self, key):
        self._logger.log_key_release(KEYBOARD_REVERSE_MAP.get(key.char if key.char is not None else key, Keyboard.KEY_UNKNOWN))

    def start_record(self):
        assert self._is_recording is False, "input recorder is already recording."

        self._is_recording = True

        self._logger.start_log()

        self._mouse_listener = mouse.Listener(on_move=self.on_move if self._record_mouse_moving else None,
                                              on_click=self.on_click, on_scroll=self.on_scroll)
        self._keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

        self._mouse_listener.start()
        self._keyboard_listener.start()

    def stop_record(self):
        if not self._is_recording:
            return

        self._is_recording = False

        self._mouse_listener.stop()
        self._keyboard_listener.stop()
        self._mouse_listener.join()
        self._keyboard_listener.join()

        self._logger.stop_log()
        for r in self._logger._records[0]:
            print(r)

    def start_replay(self):
        pass

    def stop_replay(self):
        pass
