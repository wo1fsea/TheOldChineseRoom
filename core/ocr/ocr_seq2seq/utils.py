# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/2/7
Description:
    utils.py
----------------------------------------------------------------------------"""

import itertools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from keras import backend as K
from skimage.filters import threshold_otsu


def text_to_label(text, alphabet):
    return [alphabet.index(char) for char in text]


def label_to_text(labels, alphabet):
    if isinstance(alphabet, str):
        alphabet = list(alphabet)
        alphabet.append("")

    return "".join([alphabet[c] for c in labels])


def greedy_decode(y_pred, alphabet):
    best = tuple(np.argmax(y_pred, 1))
    best = [k for k, g in itertools.groupby(best)]
    string = label_to_text(best, alphabet)
    return string


def _find_peeks(data, min_val=0, min_range=4):
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


def _binary(image):
    threshold = threshold_otsu(image)
    binary = image > threshold

    if np.sum(binary) > binary.size / 2:
        binary = 1 - binary

    return np.uint8(binary * 255)


def split_char_from_text_image(image):
    image = image.filter(ImageFilter.SHARPEN)

    image_data = np.asarray(image.convert("L"), dtype=np.uint8)
    image_data = _binary(image_data)

    h_sum = np.sum(image_data, axis=1)
    hps = _find_peeks(h_sum)

    boxes = []
    for peek_range in hps:
        start_y = peek_range[0]
        end_y = peek_range[1]
        line_img = image_data[start_y:end_y, :]
        vertical_sum = np.sum(line_img, axis=0)
        vps = _find_peeks(vertical_sum)
        boxes.append([])
        for vp in vps:
            boxes[-1].append((vp[0], start_y, vp[1], end_y))

    images = []
    for bs in boxes:
        images.append([])
        for b in bs:
            images[-1].append(image.crop(b))

    return images


def split_text_image(image, max_ratio=128 / 16):
    image = image.filter(ImageFilter.SHARPEN)

    image_data = np.asarray(image.convert("L"), dtype=np.uint8)
    image_data = _binary(image_data)
    image = Image.fromarray(image_data)

    h_sum = np.sum(image_data, axis=1)
    hps = _find_peeks(h_sum)

    boxes = []
    for peek_range in hps:
        start_y = peek_range[0]
        end_y = peek_range[1]
        line_img = image_data[start_y:end_y, :]
        vertical_sum = np.sum(line_img, axis=0)
        vps = _find_peeks(vertical_sum)
        boxes.append([])

        start_x = last_x = vps[0][0]
        max_length = (end_y - start_y) * max_ratio

        for vp in vps:
            if vp[1] - start_x > max_length:
                boxes[-1].append((start_x, start_y, last_x, end_y))
                start_x = last_x
            else:
                last_x = vp[1]

        if start_x != last_x:
            boxes[-1].append((start_x, start_y, last_x, end_y))

    images = []
    for bs in boxes:
        images.append([])
        for b in bs:
            images[-1].append(image.crop(b))

    return images


def convert_image_to_input_data(image, image_width, image_height):
    image = image.convert(mode="L")
    image_tmp = Image.new(mode="L", size=(image_width, image_height))

    bbox = image.getbbox()
    image = image.crop(bbox)

    if bbox:
        x, y, x2, y2 = bbox
        w, h = x2 - x, y2 - y
        x, y = (0, 0)

        if w / h > image_width / image_height:
            h = round(h / w * image_width)
            w = round(image_width)

        else:
            w = round(w / h * image_height)
            h = round(image_height)

        image = image.resize((w, h))
        image_tmp.paste(image, box=(x, y, x + w, y + h))

    image_data = np.asarray(image_tmp, dtype=np.uint8)
    image_data = image_data.T
    image_data = image_data.astype(np.float32) / 255

    if K.image_data_format() == 'channels_first':
        image_data = np.expand_dims(image_data, 0)
    else:
        image_data = np.expand_dims(image_data, 2)
    return image_data

def convert_input_data_to_image(image_data):
    pass


# img = Image.open("/Users/huangquanyong/Desktop/screenshot.png")
# imgs = split_text_image(img)
# for line in imgs:
#     for img in line:
#         img.show()
