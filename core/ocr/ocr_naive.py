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

import PIL
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageFilter


CHAR_SET = "1234567890-=" \
           "!@#$%^&*()_+" \
           "qwertyuiop[]\\" \
           "QWERTYUIOP{}|" \
           "asdfghjkl;'" \
           "ASDFGHJKL:\"" \
           "zxcvbnm,./" \
           "ZXCVBNM<>?"

FONT_SIZE = 100


class OCRNaive(object):
    def __init__(self):
        pass

    def image_to_string(self, image):
        return ""

    def extract_peek_ranges_from_array(self, array_vals, minimun_val=100, minimun_range=2):
        start_i = None
        end_i = None
        peek_ranges = []
        for i, val in enumerate(array_vals):
            if start_i is None:
                start_i = i
            elif val > minimun_val and start_i is not None:
                pass
            elif val <= minimun_val and start_i is not None:
                end_i = i
                if end_i - start_i >= minimun_range:
                    peek_ranges.append((start_i, end_i))
                start_i = None
                end_i = None
            elif val < minimun_val and start_i is None:
                start_i = i
            else:
                raise ValueError("cannot parse this case...")
        return peek_ranges

    def _binary(self, image):
        from skimage.filters import threshold_otsu
        # image = image.filter(ImageFilter.SHARPEN)
        # image = image.resize(map(lambda x: int(4 * x), image.size))
        image = image.convert("L")
        image = np.asarray(image, dtype=np.uint8)
        thresh = threshold_otsu(image)
        binary = image > thresh

        fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
        ax = axes.ravel()
        ax[0] = plt.subplot(1, 3, 1, adjustable='box-forced')
        ax[1] = plt.subplot(1, 3, 2)
        ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0], adjustable='box-forced')

        ax[0].imshow(image, cmap=plt.cm.gray)
        ax[0].set_title('Original')
        ax[0].axis('off')

        ax[1].hist(image.ravel(), bins=256)
        ax[1].set_title('Histogram')
        ax[1].axvline(thresh, color='r')

        ax[2].imshow(binary, cmap=plt.cm.gray)
        ax[2].set_title('Thresholded')
        ax[2].axis('off')

        plt.show()

        return Image.fromarray(np.uint8(binary*255))

    def _split_image(self, image):
        # image = image.filter(ImageFilter.SHARPEN)
        # image = image.resize(map(lambda x: int(4 * x), image.size))
        image = self._binary(image)
        image = image.convert("L")
        image.show()
        image_data = np.asarray(image, dtype=np.uint8)
        # image_data = 255 - image_data
        horizontal_sum = np.sum(image_data, axis=1)
        hps = self.extract_peek_ranges_from_array(horizontal_sum)

        image = image.convert("RGB")
        draw = ImageDraw.Draw(image)
        for s, e in hps:
            draw.line(((0, s), (image.size[0], s)), (255, 0, 0), 1)
            draw.line(((0, e), (image.size[0], e)), (255, 0, 0), 1)

        vertical_peek_ranges2d = []
        for peek_range in hps:
            start_y = peek_range[0]
            end_y = peek_range[1]
            line_img = image_data[start_y:end_y, :]
            vertical_sum = np.sum(line_img, axis=0)
            plt.plot(vertical_sum, range(vertical_sum.shape[0]))
            plt.gca().invert_yaxis()
            plt.show()
            vps = self.extract_peek_ranges_from_array(vertical_sum)
            vertical_peek_ranges2d.append(vps)

            for s, e in vps:
                draw.line(((s, start_y), (s, end_y)), (255, 0, 0), 1)
                draw.line(((e, start_y), (e, end_y)), (255, 0, 0), 1)
        image.show()
        return ""

    def _generate_data(self, char_set=CHAR_SET, font="arial.ttf"):
        data = {}
        for char in char_set:
            image = self._generate_char_data(char, font)
            data[char] = np.asarray(image, dtype=np.uint8)
        self._debug_print(data["0"])

    def _generate_char_data(self, char, font):
        image = Image.new(mode="RGBA", size=(FONT_SIZE, FONT_SIZE))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font, FONT_SIZE)
        draw.text((0, 0), char, font=font)
        bbox = image.getbbox()
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
    ocrn = OCRNaive()
    image = Image.open("ScreenClip.png")
    # ocrn._binary(image)
    ocrn._split_image(image)
