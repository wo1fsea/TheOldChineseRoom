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

from pynput import keyboard, mouse

from .keys import Keyboard, Mouse
from core.input_controller.input_recorder import InputRecorder, Logger, InputEvent
from core.input_controller.input_controller_pynput import KEYBOARD_MAP, MOUSE_MAP
from core.input_controller import InputController

KEYBOARD_REVERSE_MAP = {v: k for k, v in KEYBOARD_MAP.items()}
MOUSE_REVERSE_MAP = {v: k for k, v in MOUSE_MAP.items()}


class InputRecorderPynput(InputRecorder):
    def __init__(self, record_mouse_moving):
        self._record_mouse_moving = record_mouse_moving

        self._is_recording = False
        self._is_replaying = False

        self._mouse_listener = None
        self._keyboard_listener = None

        self._replay_thread = None

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
        if isinstance(key, keyboard.KeyCode):
            key = key.char
        self._logger.log_key_press(KEYBOARD_REVERSE_MAP.get(key, Keyboard.KEY_UNKNOWN))

    def on_release(self, key):
        if isinstance(key, keyboard.KeyCode):
            key = key.char
        self._logger.log_key_release(KEYBOARD_REVERSE_MAP.get(key, Keyboard.KEY_UNKNOWN))

    def start_record(self, record_name):
        assert self._is_recording is False, "input recorder is already recording."

        self._is_recording = True

        self._logger.start_log(record_name)

        self._mouse_listener = mouse.Listener(on_move=self.on_move if self._record_mouse_moving else None,
                                              on_click=self.on_click, on_scroll=self.on_scroll)
        self._keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

        self._mouse_listener.start()
        time.sleep(0.1)
        self._keyboard_listener.start()

    def stop_record(self):
        if not self._is_recording:
            return

        self._is_recording = False

        self._mouse_listener.stop()
        self._keyboard_listener.stop()

        self._mouse_listener.join()
        self._keyboard_listener.join()

        self._keyboard_listener = None
        self._mouse_listener = None

        self._logger.stop_log()

    def _replay_loop(self, log):
        input_controller = InputController()
        operations = {
            InputEvent.START: None,
            InputEvent.STOP: None,
            InputEvent.KEY_PRESS: input_controller.key_press,
            InputEvent.KEY_RELEASE: input_controller.key_release,
            InputEvent.MOUSE_PRESS: input_controller.mouse_press,
            InputEvent.MOUSE_RELEASE: input_controller.mouse_release,
            InputEvent.MOUSE_MOVE_TO: input_controller.mouse_move_to,
            InputEvent.MOUSE_SCROLL: input_controller.mouse_scroll,
        }
        start_time = time.time()
        for entry in log:
            t = entry[0]
            event = entry[1]
            args = entry[2:]
            func = operations.get(event)
            if not func:
                continue
            delta = time.time() - start_time
            if delta < t:
                time.sleep(t - delta)
            func(*args)

        self._is_replaying = False
        self._replay_thread = None

        return

    def start_replay(self, record_name):
        assert self._is_recording is False, "input recorder is already replaying."

        log = self._logger.get_log(record_name)
        if not log:
            return

        self._replay_thread = Thread(target=self._replay_loop, args=(log,))
        self._replay_thread.start()
        self._is_replaying = True

    def stop_replay(self):
        if not self._is_replaying:
            return

        self._replay_thread.stop()
        self._replay_thread.join()
        self._is_replaying = False

    def load_records(self, file_name):
        self._logger.load_log(file_name)

    def save_records(self, file_name):
        self._logger.save_log(file_name)
