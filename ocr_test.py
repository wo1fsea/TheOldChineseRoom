# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/11/19
Description:
    ocr_test.py
----------------------------------------------------------------------------"""

from core.ocr.ocr import OCR
from PIL import Image

if __name__ == '__main__':
    ocr = OCR("seq2seq")
    print(ocr.image_to_string(Image.open("C:/Users/wo1fsea/Desktop/ScreenClip.png")))