# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/13
Description:
    input_controller_pyautogui.py
----------------------------------------------------------------------------"""


import pyautogui

from .input_controller import InputController
from .keys import Keyboard, Mouse

PYAUTOGUI_MOUSE_MAP = {
    Mouse.BUTTON_LEFT: "left",
    Mouse.BUTTON_MIDDLE: "middle",
    Mouse.BUTTON_RIGHT: "right",
}

PYAUTOGUI_KEYBOARD_MAP = {
    Keyboard.KEY_ESCAPE: "esc",
    Keyboard.KEY_F1: "f1",
    Keyboard.KEY_F2: "f2",
    Keyboard.KEY_F3: "f3",
    Keyboard.KEY_F4: "f4",
    Keyboard.KEY_F5: "f5",
    Keyboard.KEY_F6: "f6",
    Keyboard.KEY_F7: "f7",
    Keyboard.KEY_F8: "f8",
    Keyboard.KEY_F9: "f9",
    Keyboard.KEY_F10: "f10",
    Keyboard.KEY_F11: "f11",
    Keyboard.KEY_F12: "f12",
    Keyboard.KEY_DELETE: "delete",

    Keyboard.KEY_GRAVE: "`",
    Keyboard.KEY_1: "1",
    Keyboard.KEY_2: "2",
    Keyboard.KEY_3: "3",
    Keyboard.KEY_4: "4",
    Keyboard.KEY_5: "5",
    Keyboard.KEY_6: "6",
    Keyboard.KEY_7: "7",
    Keyboard.KEY_8: "8",
    Keyboard.KEY_9: "9",
    Keyboard.KEY_0: "0",
    Keyboard.KEY_MINUS: "-",
    Keyboard.KEY_EQUALS: "=",
    Keyboard.KEY_BACKSPACE: "backspace",

    Keyboard.KEY_TAB: "tab",
    Keyboard.KEY_Q: "q",
    Keyboard.KEY_W: "w",
    Keyboard.KEY_E: "e",
    Keyboard.KEY_R: "r",
    Keyboard.KEY_T: "t",
    Keyboard.KEY_Y: "y",
    Keyboard.KEY_U: "u",
    Keyboard.KEY_I: "i",
    Keyboard.KEY_O: "o",
    Keyboard.KEY_P: "p",
    Keyboard.KEY_LEFT_BRACKET: "[",
    Keyboard.KEY_RIGHT_BRACKET: "]",
    Keyboard.KEY_BACKSLASH: "\\",

    Keyboard.KEY_CAPSLOCK: "capslock",
    Keyboard.KEY_A: "a",
    Keyboard.KEY_S: "s",
    Keyboard.KEY_D: "d",
    Keyboard.KEY_F: "f",
    Keyboard.KEY_G: "g",
    Keyboard.KEY_H: "h",
    Keyboard.KEY_J: "j",
    Keyboard.KEY_K: "k",
    Keyboard.KEY_L: "l",
    Keyboard.KEY_SEMICOLON: ";",
    Keyboard.KEY_APOSTROPHE: "'",
    Keyboard.KEY_ENTER: "enter",

    Keyboard.KEY_LEFT_SHIFT: "shiftleft",
    Keyboard.KEY_Z: "z",
    Keyboard.KEY_X: "x",
    Keyboard.KEY_C: "c",
    Keyboard.KEY_V: "v",
    Keyboard.KEY_B: "b",
    Keyboard.KEY_N: "n",
    Keyboard.KEY_M: "m",
    Keyboard.KEY_COMMA: ",",
    Keyboard.KEY_PERIOD: ".",
    Keyboard.KEY_SLASH: "/",
    Keyboard.KEY_RIGHT_SHIFT: "shiftright",

    Keyboard.KEY_LEFT_CTRL: "ctrlleft",
    Keyboard.KEY_LEFT_WINDOWS: "winleft",
    Keyboard.KEY_LEFT_ALT: "altleft",
    Keyboard.KEY_SPACE: "space",
    Keyboard.KEY_RIGHT_ALT: "altright",
    Keyboard.KEY_RIGHT_CTRL: "ctrlright",

    Keyboard.KEY_UP: "up",
    Keyboard.KEY_LEFT: "left",
    Keyboard.KEY_DOWN: "down",
    Keyboard.KEY_RIGHT: "right",
}


class InputControllerPyautogui(InputController):
    def __init__(self):
        pass

    def key_press(self, key):
        pyautogui.keyDown(PYAUTOGUI_KEYBOARD_MAP[key])

    def key_release(self, key):
        pyautogui.keyUp(PYAUTOGUI_KEYBOARD_MAP[key])

    def key_tap(self, key):
        pyautogui.press(PYAUTOGUI_KEYBOARD_MAP[key])

    def mouse_press(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        pyautogui.mouseDown(button=PYAUTOGUI_MOUSE_MAP[button], x=position[0], y=position[1])

    def mouse_release(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        pyautogui.mouseUp(button=PYAUTOGUI_MOUSE_MAP[button], x=position[0], y=position[1])

    def mouse_click(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        pyautogui.click(button=PYAUTOGUI_MOUSE_MAP[button], x=position[0], y=position[1])

    def mouse_move_to(self, position):
        pyautogui.moveTo(x=position[0], y=position[1])

    def mouse_scroll(self, amount, position=(None, None)):
        pyautogui.mouse_scroll(amount, x=position[0], y=position[1])

    @property
    def mouse_position(self):
        return pyautogui.position()

    @property
    def screen_size(self):
        return pyautogui.size()
