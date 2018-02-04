# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/11/18
Description:
    ocr_naive.py
----------------------------------------------------------------------------"""

# from .ocr import OCR

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu

CHAR_SET = "1234567890-=" \
           "!@#$%^&*()_+" \
           "qwertyuiop[]\\" \
           "QWERTYUIOP{}|" \
           "asdfghjkl;'" \
           "ASDFGHJKL:\"" \
           "zxcvbnm,./" \
           "ZXCVBNM<>?"

CHAR_SET_NUM = "+-1234567890.,"

FONT_SIZE = 100


class OCRNaive(object):
    def __init__(self, char_set=CHAR_SET, font="/Users/huangquanyong/Documents/GitHub/TheChineseRoom/core/ocr/Arial.ttf"):
        self._base_data = {}
        self._generate_data(char_set, font)

    def image_to_string(self, image):
        return ""

    def _find_peeks(self, data, min_val=0, min_range=1):
        start = None
        peeks = []
        for i, val in enumerate(data):
            if val > min_val:
                if start is None:
                    start = i
            else:
                if start is not None:
                    if i - start >= min_range:
                        peeks.append((start, i))
                    start = None

        return peeks

    def _binary(self, image):
        # image = image.filter(ImageFilter.SHARPEN)
        # image = image.resize(map(lambda x: int(4 * x), image.size))

        threshold = threshold_otsu(image)
        binary = image > threshold

        if np.sum(binary) > binary.size / 2:
            binary = 1 - binary

        # binary = image * binary

        # fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
        # ax = axes.ravel()
        # ax[0] = plt.subplot(1, 3, 1, adjustable='box-forced')
        # ax[1] = plt.subplot(1, 3, 2)
        # ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0], adjustable='box-forced')
        #
        # ax[0].imshow(image, cmap=plt.cm.gray)
        # ax[0].set_title('Original')
        # ax[0].axis('off')
        #
        # ax[1].hist(image.ravel(), bins=256)
        # ax[1].set_title('Histogram')
        # ax[1].axvline(thresh, color='r')
        #
        # ax[2].imshow(binary, cmap=plt.cm.gray)
        # ax[2].set_title('Thresholded')
        # ax[2].axis('off')
        #
        # plt.show()

        return np.uint8(binary * 255)

    def r(self, image):
        images = self._split_image(image)
        string = ""
        for imgs in images:
            for img in imgs:
                string += self._match_char(img)
            string += "\n"
        return string

    def _split_image(self, image):
        image = image.filter(ImageFilter.SHARPEN)
        # image = image.resize(map(lambda x: int(4 * x), image.size))

        image_data = np.asarray(image.convert("L"), dtype=np.uint8)
        image_data = self._binary(image_data)

        h_sum = np.sum(image_data, axis=1)
        hps = self._find_peeks(h_sum)

        boxes = []
        for peek_range in hps:
            start_y = peek_range[0]
            end_y = peek_range[1]
            line_img = image_data[start_y:end_y, :]
            vertical_sum = np.sum(line_img, axis=0)
            # plt.plot(vertical_sum, range(vertical_sum.shape[0]))
            # plt.gca().invert_yaxis()
            # plt.show()
            vps = self._find_peeks(vertical_sum)
            boxes.append([])
            for vp in vps:
                boxes[-1].append((vp[0], start_y, vp[1], end_y))

        image2 = Image.fromarray(image_data)
        image2.show()
        image2 = image2.convert("RGB")
        draw = ImageDraw.Draw(image2)
        for bs in boxes:
            for b in bs:
                draw.rectangle(b, outline=(255, 0, 0))
        image2.show()

        images = []
        for bs in boxes:
            images.append([])
            for b in bs:
                images[-1].append(image.crop(b))

        return images

    def _match_char(self, image):
        image = image.convert("L")
        image_data = np.asarray(image, dtype=np.int32)
        image_data = self._binary(image_data)
        # if np.sum(image_data) > image_data.size * 255 / 2:
        #     image_data = 255 - image_data

        image = Image.fromarray(image_data)
        bbox = image.getbbox()
        # bbox = (bbox[0], 0, bbox[2], image.size[1])

        image = image.crop(bbox)
        image = image.resize((FONT_SIZE, FONT_SIZE))
        # image.show()
        image_data = np.asarray(image, dtype=np.int32)

        min_c = "0"
        min_d = np.sum((image_data - self._base_data[min_c]) ** 2)
        for c, data in self._base_data.items():
            d = np.sum((image_data - data) ** 2)
            if d < min_d:
                print(c, d)
                min_d = d
                min_c = c
        return min_c

    def _generate_data(self, char_set, font):
        data = {}
        for char in char_set:
            image = self._generate_char_data(char, font)
            data[char] = np.asarray(image, dtype=np.uint8)

        self._base_data = data

    def _generate_char_data(self, char, font):
        image = Image.new(mode="RGBA", size=(FONT_SIZE, FONT_SIZE))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font, FONT_SIZE)
        draw.text((0, 0), char, font=font)
        # image.show()
        bbox = image.getbbox()
        # bbox = (bbox[0], 0, bbox[2], 100)
        image = image.crop(bbox)
        image = image.convert("L")
        image = image.resize((FONT_SIZE, FONT_SIZE))
        return image

    def _debug_print(self, image_data):
        w, h = image_data.shape
        for i in range(w):
            s = ""
            for j in range(h):
                s += " " + str(image_data[i][j])
            print(s)


if __name__ == '__main__':
    ocrn = OCRNaive(CHAR_SET_NUM)
    img = Image.open("ScreenClip2.png")
    string = ocrn.r(img)
    print(string)

    # imgs = ocrn._split_image(img)
    # c = ocrn._match_char(imgs[0][2])
    # Image.fromarray(ocrn._base_data["2"]).show()
    # Image.fromarray(ocrn._base_data[c]).show()
    # print(c)