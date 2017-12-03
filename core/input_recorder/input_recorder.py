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

from utils.singleton import Singleton

DEFAULT_BACKEND = "pyautogui"


class InputRecorder(Singleton):
    def __init__(self, backend=DEFAULT_BACKEND):
        super(InputRecorder, self).__init__()
        self._adapter = self._load_adapter()(backend)

    def start_record(self):
        self._adapter.start_record()

    def stop_record(self):
        self._adapter.stop_record()

    def start_replay(self):
        self._adapter.start_replay()

    def stop_replay(self):
        self._adapter.stop_replay()

    def _load_adapter(self, backend):
        pass