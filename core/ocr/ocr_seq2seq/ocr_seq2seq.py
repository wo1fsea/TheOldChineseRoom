# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/2/11
Description:
    ocr_seq2seq.py
----------------------------------------------------------------------------"""
from PIL import Image
import numpy as np
from ..ocr import OCR
from .ocr_model import OCRModel
from .utils import split_text_image, convert_image_to_input_data

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 16


class OCRSeq2Seq(OCR):
    MIN_SIZE = 256.

    def __init__(self):
        self._ocr_model = OCRModel(IMAGE_WIDTH, IMAGE_HEIGHT)

    def image_to_string(self, image):
        self._ocr_model.load_config_for_predict_model(r"D:\GITHUB\TheChineseRoom\ocr_model\checkpoint_27")
        img = Image.open("C:/Users/wo1fsea/Desktop/ScreenClip.png")

        imgs = split_text_image(img, IMAGE_WIDTH / IMAGE_HEIGHT)
        input_data = []
        for line in imgs:
            for img in line:
                input_data.append(convert_image_to_input_data(img, IMAGE_WIDTH, IMAGE_HEIGHT))
                img.show()

        size = len(input_data)
        input = np.ones([size, *(input_data[0].shape)])

        for i, data in enumerate(input_data):
            input[i] = data

        strings = self._ocr_model.predict(input)

        result = ""
        i = 0
        for line in imgs:
            for img in line:
                result += strings[i]
                i += 1

            result += "\n"

        return result