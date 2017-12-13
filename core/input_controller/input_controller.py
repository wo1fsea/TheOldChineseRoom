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

DEFAULT_BACKEND = "pynput"


class InputController(Singleton):
    def __init__(self, backend=DEFAULT_BACKEND):
        super(InputController, self).__init__()
        self._adapter = self._load_adapter(backend)()

    def key_press(self, key):
        self._adapter.key_press(key)

    def key_release(self, key):
        self._adapter.key_release(key)

    def key_tap(self, key):
        self.key_tap(key)

    def mouse_press(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        self._adapter.mouse_press(button, position)

    def mouse_release(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        self._adapter.mouse_release(button, position)

    def mouse_click(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        self._adapter.mouse_click(button, position)

    def mouse_move_to(self, position):
        self._adapter.mouse_move_to(position)

    def mouse_scroll(self, amount, position=(None, None)):
        self._adapter.mouse_scroll(amount, position)

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
        elif backend == "pynput":
            from .input_controller_pynput import InputControllerPynput
            return InputControllerPynput
        else:
            raise NotImplementedError()
