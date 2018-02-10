# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/1/22
Description:
    image_generator.py
----------------------------------------------------------------------------"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from keras.preprocessing import image as kpImage
from scipy import ndimage
import math
import random
from keras import backend as K

FONT_SIZE = 32
ROTATION_DEGREE = 5


class ImageGenerator(object):

    def __init__(self, width, height, font_set):
        super(ImageGenerator, self).__init__()
        self.width = width
        self.height = height
        self.font_set = font_set
        self.font_size = FONT_SIZE

    def add_noise(self, image):
        row, col = image.shape
        mean = 0
        var = 0.1
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col)) * 128
        noisy = image + gauss
        noisy[noisy < 0] = 0
        noisy[noisy > 255] = 255
        return noisy.astype(np.uint8)

    def generate(self, string, rotation=False, translate=False, noise=False):
        """

        :param string:
        :param rotation:
        :param translate:
        :param noise:
        :return:
        """
        font = np.random.choice(self.font_set)
        font_size = self.font_size

        image = Image.new(mode="RGB", size=(self.width, self.height))
        image_tmp = Image.new(mode="RGB", size=(font_size * len(string), 2 * font_size))
        draw = ImageDraw.Draw(image_tmp)
        font = ImageFont.truetype(font, font_size)
        draw.text((0, 0), string, font=font)

        if rotation:
            image_tmp = image_tmp.rotate(ROTATION_DEGREE * (np.random.random() - 0.5) * 2, expand=True)

        bbox = image_tmp.getbbox()
        image_tmp = image_tmp.crop(bbox)

        if bbox:
            x, y, x2, y2 = bbox
            w, h = x2 - x, y2 - y

            if w / h > self.width / self.height:
                h = round(h / w * self.width)
                w = round(self.width)
                x, y = (0, round(np.random.random() * (self.height - h))) if translate else (0, 0)
            else:
                w = round(w / h * self.height)
                h = round(self.height)
                x, y = (round(np.random.random() * (self.width - w)), 0) if translate else (0, 0)

            image_tmp = image_tmp.resize((w, h))

            image.paste(image_tmp, box=(x, y, x + w, y + h))

        image = image.convert(mode="L")
        image_array = np.asarray(image, dtype=np.uint8)

        if noise:
            image_array = self.add_noise(image_array)

        return image_array
