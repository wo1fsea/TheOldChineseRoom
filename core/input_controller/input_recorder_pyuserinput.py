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

from pykeyboard import PyKeyboardEvent
from pymouse import PyMouseEvent

from core.input_controller.input_recorder import InputRecorder
from core.input_controller.input_controller_pyuserinput import PYUSERINPUT_KEYBOARD_MAP, PYUSERINPUT_MOUSE_MAP

PYUSERINPUT_KEYBOARD_REVERSE_MAP = {v: k for k, v in PYUSERINPUT_KEYBOARD_MAP.items()}
PYUSERINPUT_MOUSE_MAP = {v: k for k, v in PYUSERINPUT_MOUSE_MAP.items()}


class MouseListener(PyMouseEvent):
    def __init__(self, record_mouse_moving=False):
        super(MouseListener, self).__init__(capture_move=record_mouse_moving)
        self._record_mouse_moving = record_mouse_moving

    def click(self, x, y, button, press):
        print(x, y)

    def move(self, x, y):
        if self._record_mouse_moving:
            print(x, y)

    def scroll(self, x, y, v, h):
        print(x, y)


class KeyboardListener(PyKeyboardEvent):
    def __init__(self):
        super(KeyboardListener, self).__init__()

    # fix pykeyboardevent bug on mac
    def key_press(self, key):
        from pykeyboard.mac import key_code_translate_table
        self.tap(key, key_code_translate_table[key], True)

    def key_release(self, key):
        from pykeyboard.mac import key_code_translate_table
        self.tap(key, key_code_translate_table[key], False)

    def tap(self, keycode, character, press):
        print(character)
        print("tap", keycode, PYUSERINPUT_KEYBOARD_REVERSE_MAP.get(character) or PYUSERINPUT_KEYBOARD_REVERSE_MAP.get(keycode) or character, press)


class InputRecorderPyuserinput(InputRecorder):
    def __init__(self, record_mouse_moving):
        self._record_mouse_moving = record_mouse_moving
        self._is_recording = False
        self._mouse_listener = None
        self._mouse_record_thread = None
        self._keyboard_listener = None
        self._keyboard_record_thread = None

    def start_record(self):
        assert self._is_recording is False, "input recorder is already recording."
        self._is_recording = True

        self._mouse_listener = MouseListener(self._record_mouse_moving)
        self._keyboard_listener = KeyboardListener()

        self._mouse_record_thread = Thread(target=self._mouse_listener.run)
        self._mouse_record_thread.start()

        time.sleep(0.1)

        self._keyboard_record_thread = Thread(target=self._keyboard_listener.run)
        self._keyboard_record_thread.start()

    def stop_record(self):
        if not self._is_recording:
            return

        self._is_recording = False

        self._mouse_listener.stop()
        self._mouse_listener = None
        self._mouse_record_thread.join()

        self._keyboard_listener.stop()
        self._keyboard_listener = None
        self._keyboard_record_thread.join()

    def start_replay(self):
        pass

    def stop_replay(self):
        pass
