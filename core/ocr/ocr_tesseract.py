# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/7
Description:
    ocr_tesseract.py
----------------------------------------------------------------------------"""

from .ocr import OCR
import os
import sys
import subprocess
from PIL import Image

WIN32_TESSERACT_PATH = "C:\\Program Files (x86)\\Tesseract-OCR"
WIN32_TESSERACT_BIN = "tesseract.exe"

DARWIN_TESSERACT_PATH = ""
DARWIN_TESSERACT_BIN = "tesseract"

if sys.platform == "darwin":
    TESSERACT_COMMAND = os.path.join(DARWIN_TESSERACT_PATH, DARWIN_TESSERACT_BIN)
elif sys.platform == "win32":
    TESSERACT_COMMAND = os.path.join(WIN32_TESSERACT_PATH, WIN32_TESSERACT_BIN)
else:
    raise NotImplementedError()

TEMP_INPUT_FILE = "tmp_input.bmp"
TEMP_OUTPUT_FILE = "tmp_output.txt"


class OCRTesseract(OCR):
    MIN_SIZE = 256.

    def __init__(self):
        pass

    def image_to_string(self, image):
        if min(image.size) < self.MIN_SIZE:
            scale = self.MIN_SIZE / image.size[0] if image.size[0] < image.size[1] else self.MIN_SIZE / image.size[1]
            image = image.resize(map(lambda x: int(scale * x), image.size), Image.LANCZOS)

        return self._image_to_string(image)

    def _image_to_string(self, image):
        image.save(TEMP_INPUT_FILE)
        subprocess.check_call([TESSERACT_COMMAND, TEMP_INPUT_FILE, os.path.splitext(TEMP_OUTPUT_FILE)[0]])
        with open(TEMP_OUTPUT_FILE) as fp:
            return fp.read()

