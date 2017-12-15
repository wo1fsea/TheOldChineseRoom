# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/12/3
Description:
    input_controller_pyuserinput.py
----------------------------------------------------------------------------"""

from pynput import mouse
from pynput import keyboard

_keyboard = keyboard.Controller()
_mouse = mouse.Controller()

from .input_controller import InputController
from .keys import Keyboard, Mouse

MOUSE_MAP = {
    Mouse.BUTTON_LEFT: mouse.Button.left,
    Mouse.BUTTON_MIDDLE: mouse.Button.middle,
    Mouse.BUTTON_RIGHT: mouse.Button.right,
}

KEYBOARD_MAP = {
    Keyboard.KEY_ESCAPE: keyboard.Key.esc,
    Keyboard.KEY_F1: keyboard.Key.f1,
    Keyboard.KEY_F2: keyboard.Key.f2,
    Keyboard.KEY_F3: keyboard.Key.f3,
    Keyboard.KEY_F4: keyboard.Key.f4,
    Keyboard.KEY_F5: keyboard.Key.f5,
    Keyboard.KEY_F6: keyboard.Key.f6,
    Keyboard.KEY_F7: keyboard.Key.f7,
    Keyboard.KEY_F8: keyboard.Key.f8,
    Keyboard.KEY_F9: keyboard.Key.f9,
    Keyboard.KEY_F10: keyboard.Key.f10,
    Keyboard.KEY_F11: keyboard.Key.f11,
    Keyboard.KEY_F12: keyboard.Key.f12,
    Keyboard.KEY_DELETE: keyboard.Key.delete,

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
    Keyboard.KEY_BACKSPACE: keyboard.Key.backspace,

    Keyboard.KEY_TAB: keyboard.Key.tab,
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

    Keyboard.KEY_CAPSLOCK: keyboard.Key.caps_lock,
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
    Keyboard.KEY_ENTER: keyboard.Key.enter,

    Keyboard.KEY_LEFT_SHIFT: keyboard.Key.shift_l,
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
    Keyboard.KEY_RIGHT_SHIFT: keyboard.Key.shift_r,

    Keyboard.KEY_LEFT_CTRL: keyboard.Key.ctrl_l,
    Keyboard.KEY_LEFT_WINDOWS: keyboard.Key.cmd_l,
    Keyboard.KEY_LEFT_ALT: keyboard.Key.alt_l,
    Keyboard.KEY_SPACE: keyboard.Key.space,
    Keyboard.KEY_RIGHT_ALT: keyboard.Key.alt_r,
    Keyboard.KEY_RIGHT_CTRL: keyboard.Key.ctrl_r,

    Keyboard.KEY_UP: keyboard.Key.up,
    Keyboard.KEY_LEFT: keyboard.Key.left,
    Keyboard.KEY_DOWN: keyboard.Key.down,
    Keyboard.KEY_RIGHT: keyboard.Key.right,

    # Keyboard.KEY_INSERT: keyboard.Key.insert,
    # Keyboard.KEY_PRINT_SCREEN: keyboard.Key.print_screen,
    # Keyboard.KEY_SCROLL_LOCK: keyboard.Key.scroll_lock,
    # Keyboard.KEY_PAUSE: keyboard.Key.pause,
    Keyboard.KEY_HOME: keyboard.Key.home,
    Keyboard.KEY_END: keyboard.Key.end,
    Keyboard.KEY_PAGE_UP: keyboard.Key.page_up,
    Keyboard.KEY_PAGE_DOWN: keyboard.Key.page_down,

    Keyboard.KEY_UNKNOWN: None,
}


class InputControllerPynput(InputController):
    def __init__(self):
        pass

    def key_press(self, key):
        _keyboard.press(KEYBOARD_MAP[key])

    def key_release(self, key):
        _keyboard.release(KEYBOARD_MAP[key])

    def key_tap(self, key):
        _keyboard.press(KEYBOARD_MAP[key])
        _keyboard.release(KEYBOARD_MAP[key])

    def mouse_press(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        if position[0] is not None:
            _mouse.position = position
        _mouse.press(MOUSE_MAP[button])

    def mouse_release(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        if position[0] is not None:
            _mouse.position = position
        _mouse.release(MOUSE_MAP[button])

    def mouse_click(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        if position[0] is not None:
            _mouse.position = position
        _mouse.click(MOUSE_MAP[button])

    def mouse_move_to(self, position):
        _mouse.position = position

    def mouse_scroll(self, amount, position=(None, None)):
        if position[0] is not None:
            _mouse.position = position
        _mouse.scroll(0, amount)

    @property
    def mouse_position(self):
        return _mouse.position

    @property
    def screen_size(self):
        pass
        # return _mouse.screen_size()
