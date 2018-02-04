# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/2/4
Description:
    ocr_model_test1.py
----------------------------------------------------------------------------"""

from core.ocr.ocr_seq2seq.ocr_model import OCRModel

ocr_m = OCRModel(128, 16)
ocr_m.train(0, 2)