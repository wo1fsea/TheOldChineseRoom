# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/7
Description:
    ocr.py
----------------------------------------------------------------------------"""

import pytesseract
from PIL import Image

MIN_SIZE = 256.


def image_to_string(image):
    if min(image.size) < MIN_SIZE:
        scale = MIN_SIZE / image.size[0] if image.size[0] < image.size[1] else MIN_SIZE / image.size[1]
        image = image.resize(map(lambda x: int(scale * x), image.size), Image.LANCZOS)

    return pytesseract.image_to_string(image)


def main():
    return image_to_string(Image.open("/Users/huangquanyong/Desktop/2.png"))


if __name__ == '__main__':
    main()
