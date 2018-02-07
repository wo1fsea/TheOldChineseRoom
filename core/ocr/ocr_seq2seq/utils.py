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
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from skimage.filters import threshold_otsu

def text_to_label(text, alphabet):
	return [alphabet.index(char) for char in text]


def label_to_text(labels, alphabet):
	if isinstance(alphabet, str):
		alphabet = list(alphabet)
		alphabet.append("")

	return "".join([alphabet[c] for c in labels])


def greedy_decode(y_pred, alphabet):
	out_best = tuple(np.argmax(y_pred, 1))
	out_best = [k for k, g in itertools.groupby(out_best)]
	string = label_to_text(out_best, alphabet)
	return string


def _find_peeks(data, min_val=0, min_range=1):
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


def _split_image(image):
	image = image.filter(ImageFilter.SHARPEN)
	# image = image.resize(map(lambda x: int(4 * x), image.size))

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
		# plt.plot(vertical_sum, range(vertical_sum.shape[0]))
		# plt.gca().invert_yaxis()
		# plt.show()
		vps = _find_peeks(vertical_sum)
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


img = Image.open("C:\\Users\\gzhuangquanyong\\Desktop\\ScreenClip.png")
_split_image(img)