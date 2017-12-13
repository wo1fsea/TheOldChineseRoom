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
import json

from utils.singleton import Singleton

DEFAULT_BACKEND = "pynput"


class InputRecorder(Singleton):
    def __init__(self, record_mouse_moving=False, backend=DEFAULT_BACKEND):
        super(InputRecorder, self).__init__()
        self._adapter = self._load_adapter(backend)(record_mouse_moving=record_mouse_moving)

    def start_record(self, record_name):
        self._adapter.start_record(record_name)

    def stop_record(self):
        self._adapter.stop_record()

    def start_replay(self, record_name):
        self._adapter.start_replay(record_name)

    def stop_replay(self):
        self._adapter.stop_replay()

    def load_records(self, file_name):
        self._adapter.load_records(file_name)

    def save_records(self, file_name):
        self._adapter.save_records(file_name)

    def _load_adapter(self, backend):
        if backend == "pyuserinput":
            from .input_recorder_pyuserinput import InputRecorderPyuserinput
            return InputRecorderPyuserinput
        elif backend == "pynput":
            from .input_recorder_pynput import InputRecorderPynput
            return InputRecorderPynput
        else:
            raise NotImplementedError()


class InputEvent:
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
        self._logs = {}
        self._data = None
        self._is_logging = False
        self._start_time = None
        self._cur_log_name = None

    def start_log(self, log_name):
        self._is_logging = True
        self._start_time = time.time()
        self._cur_log_name = log_name

        self._data = []
        self._data.append((0, InputEvent.START,))

    def stop_log(self):
        self._data.append((time.time() - self._start_time, InputEvent.STOP,))
        self._logs[self._cur_log_name] = self._data

        self._is_logging = False
        self._cur_log_name = None
        self._data = None
        self._start_time = None

    def is_logging(self):
        return self._is_logging

    def get_log(self, log_name):
        return self._logs.get(log_name)

    def delete_log(self, log_name):
        if log_name in self._logs:
            del self._logs[log_name]

    def get_cur_record_name(self):
        return self._cur_log_name

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
        self._data.append((time.time() - self._start_time, InputEvent.MOUSE_SCROLL, amount, position))

    def save_log(self, file_name):
        with open(file_name, "w") as fp:
            json.dump(self._logs, fp, indent=2)

    def load_log(self, file_name):
        with open(file_name) as fp:
            self._logs = json.load(fp)
