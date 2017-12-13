# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/12/3
Description:
    input_recorder_test.py
----------------------------------------------------------------------------"""

import time
from core.input_controller import InputRecorder


ir = InputRecorder(True)
ir.start_record("A")
time.sleep(10)
ir.stop_record()
ir.save_records("DDD")
ir.start_replay("A")
