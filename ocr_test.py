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
    ocr = OCR()
    print(ocr.image_to_string(Image.open('core/ocr/ScreenClip.png')))