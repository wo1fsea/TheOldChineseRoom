# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong (wo1fSea)
	quanyongh@foxmail.com
Date:
	2017/10/13
Description:
	output.py
----------------------------------------------------------------------------"""

from utils.singleton import Singleton
import pyautogui


class OutputManager(Singleton):
	def __init__(self):
		super(OutputManager, self).__init__()

	def key_down(self):
		pass

	def key_up(self):
		pass

	def key_press(self):
		pass

	def mouse_down(self):
		pass

	def mouse_up(self):
		pass

	def mouse_click(self):
		pass

	def mouse_move_to(self):
		pass

	def scroll(self):
		pass

	@property
	def mouse_position(self):
		return pyautogui.position()

	@property
	def screen_size(self):
		return pyautogui.size()