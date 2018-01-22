# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong
	gzhuangquanyong@corp.netease.com
Date:
	2018/1/22
Description:
	image_generator.py
----------------------------------------------------------------------------"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from keras.preprocessing import image as kpImage
from scipy import ndimage
import numpy as np
from keras import backend as K

CHAR_SET = "1234567890-=" \
           "!@#$%^&*()_+" \
           "qwertyuiop[]\\" \
           "QWERTYUIOP{}|" \
           "asdfghjkl;'" \
           "ASDFGHJKL:\"" \
           "zxcvbnm,./" \
           "ZXCVBNM<>?"

CHAR_SET_NUM = "+-1234567890.,"
FONT_SIZE = 32
FONT = "arial.ttf"


class ImageGenerator(object):

	def __init__(self):
		pass

	def generate(self, string, font=FONT, font_size=FONT_SIZE):
		"""

		:param string:
		:param font:
		:param font_size:
		:return:
		"""

		image = Image.new(mode="RGB", size=(FONT_SIZE * len(string), FONT_SIZE))
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype(font, FONT_SIZE)
		draw.text((0, 0), string, font=font)
		bbox = image.getbbox()
		image = image.crop(bbox)
		x, y, x2, y2 = bbox
		w, h = x2 - x, y2 - y
		print(bbox)
		imageBig = Image.new(mode="RGB", size=(w * 2, h * 2))
		imageBig.paste(image, box=(round(w / 2), round(h / 2), round(w / 2) + w, round(h / 2) + h))
		image_array = np.asarray(imageBig, dtype=np.uint8)
		image = Image.fromarray(kpImage.random_rotation(image_array, 5, row_axis=0, col_axis=1, channel_axis=2))
		image.save("a.png")

	def a(self):
		pass


#
#
# np.random.seed(55)
#
#
# # this creates larger "blotches" of noise which look
# # more realistic than just adding gaussian noise
# # assumes greyscale with pixels ranging from 0 to 1
#
# def speckle(img):
# 	severity = np.random.uniform(0, 0.6)
# 	blur = ndimage.gaussian_filter(np.random.randn(*img.shape) * severity, 1)
# 	img_speck = (img + blur)
# 	img_speck[img_speck > 1] = 1
# 	img_speck[img_speck <= 0] = 0
# 	return img_speck
#
#
# # paints the string in a random location the bounding box
# # also uses a random font, a slight random rotation,
# # and a random amount of speckle noise
#
# def paint_text(text, w, h, rotate=False, ud=False, multi_fonts=False):
# 	surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
# 	with cairo.Context(surface) as context:
# 		context.set_source_rgb(1, 1, 1)  # White
# 		context.paint()
# 		# this font list works in CentOS 7
# 		if multi_fonts:
# 			fonts = ['Century Schoolbook', 'Courier', 'STIX', 'URW Chancery L', 'FreeMono']
# 			context.select_font_face(np.random.choice(fonts), cairo.FONT_SLANT_NORMAL,
# 			                         np.random.choice([cairo.FONT_WEIGHT_BOLD, cairo.FONT_WEIGHT_NORMAL]))
# 		else:
# 			context.select_font_face('Courier', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
# 		context.set_font_size(25)
# 		box = context.text_extents(text)
# 		border_w_h = (4, 4)
# 		if box[2] > (w - 2 * border_w_h[1]) or box[3] > (h - 2 * border_w_h[0]):
# 			raise IOError('Could not fit string into image. Max char count is too large for given image width.')
#
# 		# teach the RNN translational invariance by
# 		# fitting text box randomly on canvas, with some room to rotate
# 		max_shift_x = w - box[2] - border_w_h[0]
# 		max_shift_y = h - box[3] - border_w_h[1]
# 		top_left_x = np.random.randint(0, int(max_shift_x))
# 		if ud:
# 			top_left_y = np.random.randint(0, int(max_shift_y))
# 		else:
# 			top_left_y = h // 2
# 		context.move_to(top_left_x - int(box[0]), top_left_y - int(box[1]))
# 		context.set_source_rgb(0, 0, 0)
# 		context.show_text(text)
#
# 	buf = surface.get_data()
# 	a = np.frombuffer(buf, np.uint8)
# 	a.shape = (h, w, 4)
# 	a = a[:, :, 0]  # grab single channel
# 	a = a.astype(np.float32) / 255
# 	a = np.expand_dims(a, 0)
# 	if rotate:
# 		a = image.random_rotation(a, 3 * (w - top_left_x) / w + 1)
# 	a = speckle(a)
#
# 	return a
#
#
# class

ig = ImageGenerator()
ig.generate("AAAAAAAA")
