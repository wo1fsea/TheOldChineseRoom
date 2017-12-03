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


from .input_recorder import InputRecorder

class InputRecorderPyuserinput(InputRecorder):
    def __init__(self):
        pass

    def start_record(self):


    def stop_record(self):
        self._adapter.stop_record()

    def start_replay(self):
        self._adapter.start_replay()

    def stop_replay(self):
        self._adapter.stop_replay()

    def _load_adapter(self, backend):
        pass