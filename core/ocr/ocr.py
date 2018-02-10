# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/11/18
Description:
    ocr.py
----------------------------------------------------------------------------"""


class OCR(object):
    def __init__(self, implement="pytesseract"):
        super(OCR, self).__init__()
        self._adapter = self._load_adapter(implement)

    def image_to_string(self, image):
        return self._adapter.image_to_string(image)

    def _load_adapter(self, implement):
        if implement == "pytesseract":
            from .ocr_tesseract import OCRTesseract
            return OCRTesseract()
        if implement == "naive":
            from .ocr_naive import OCRNaive
            return OCRNaive()
        if implement == "seq2seq":
            from .ocr_seq2seq import OCRSeq2Seq
            return OCRSeq2Seq()
        else:
            raise NotImplementedError
