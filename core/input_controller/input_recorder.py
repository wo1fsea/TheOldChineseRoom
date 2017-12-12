# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/12/3
Description:
    input_recorder.py
----------------------------------------------------------------------------"""

import time

from utils.singleton import Singleton
from enum import Enum

DEFAULT_BACKEND = "pynput"


class InputEvent(Enum):
    START = "START"
    STOP = "STOP"
    KEY_PRESS = "KEY_PRESS"
    KEY_RELEASE = "KEY_RELEASE"
    MOUSE_PRESS = "MOUSE_PRESS"
    MOUSE_RELEASE = "MOUSE_RELEASE"
    MOUSE_MOVE_TO = "MOUSE_MOVE_TO"
    MOUSE_SCROLL = "MOUSE_SCROLL"


class Logger(object):
    def __init__(self):
        self._is_logging = False
        self._records = []
        self._data = None
        self._start_time = None

    def start_log(self):
        self._is_logging = True
        self._start_time = time.time()
        self._data = []
        self._data.append((0, InputEvent.START, ))

    def stop_log(self):
        self._data.append((time.time() - self._start_time, InputEvent.STOP, ))
        self._records.append(self._data)
        self._data = None
        self._start_time = None

    def log_key_press(self, key):
        self._data.append((time.time() - self._start_time, InputEvent.KEY_PRESS, key))

    def log_key_release(self, key):
        self._data.append((time.time() - self._start_time, InputEvent.KEY_RELEASE, key))

    def log_mouse_press(self, button, position):
        self._data.append((time.time() - self._start_time, InputEvent.MOUSE_PRESS, button, position))

    def log_mouse_release(self, button, position):
        self._data.append((time.time() - self._start_time, InputEvent.MOUSE_RELEASE, button, position))

    def log_mouse_move_to(self, position):
        self._data.append((time.time() - self._start_time, InputEvent.MOUSE_MOVE_TO, position))

    def log_mouse_scroll(self, amount, position):
        self._data.append((time.time() - self._start_time, InputEvent.MOUSE_RELEASE, amount, position))


class InputRecorder(Singleton):
    def __init__(self, record_mouse_moving=False, backend=DEFAULT_BACKEND):
        super(InputRecorder, self).__init__()
        self._adapter = self._load_adapter(backend)(record_mouse_moving=record_mouse_moving)

    def start_record(self):
        self._adapter.start_record()

    def stop_record(self):
        self._adapter.stop_record()

    def start_replay(self):
        self._adapter.start_replay()

    def stop_replay(self):
        self._adapter.stop_replay()

    def _load_adapter(self, backend):
        if backend == "pyuserinput":
            from .input_recorder_pyuserinput import InputRecorderPyuserinput
            return InputRecorderPyuserinput
        elif backend == "pynput":
            from .input_recorder_pynput import InputRecorderPynput
            return InputRecorderPynput
        else:
            raise NotImplementedError()
