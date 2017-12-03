# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/12/3
Description:
    input_controller.py
----------------------------------------------------------------------------"""

from utils.singleton import Singleton
from .keys import Mouse

DEFAULT_BACKEND = "pyautogui"


class InputController(Singleton):
    def __init__(self, backend=DEFAULT_BACKEND):
        super(InputController, self).__init__()
        self._adapter = self._load_adapter()(backend)

    def key_down(self, key):
        self._adapter.key_down(key)

    def key_up(self, key):
        self._adapter.key_up(key)

    def key_press(self, key):
        self.key_press(key)

    def mouse_down(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        self._adapter.mouse_down(button, position)

    def mouse_up(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        self._adapter.mouse_up(button, position)

    def mouse_click(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        self._adapter.mouse_click(button, position)

    def mouse_move_to(self, position):
        self._adapter.mouse_move_to(position)

    def scroll(self, amount, position=(None, None)):
        self._adapter.scroll(amount, position)

    @property
    def mouse_position(self):
        return self._adapter.mouse_position()

    @property
    def screen_size(self):
        return self._adapter.screen_size()

    def _load_adapter(self, backend):
        if backend == "pyautogui":
            from .input_controller_pyautogui import InputControllerPyautogui
            return InputControllerPyautogui
        elif backend == "pyuserinput":
            from .input_controller_pyuserinput import InputControllerPyuserinput
            return InputControllerPyuserinput
        else:
            raise NotImplementedError()
