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

from pymouse import PyMouse
from pykeyboard import PyKeyboard

from .input_controller import InputController
from .keys import Keyboard, Mouse

_mouse = PyMouse()
_keyboard = PyKeyboard()

PYUSERINPUT_MOUSE_MAP = {
    Mouse.BUTTON_LEFT: 1,
    Mouse.BUTTON_MIDDLE: 3,
    Mouse.BUTTON_RIGHT: 2,
}

PYUSERINPUT_KEYBOARD_MAP = {
    Keyboard.KEY_ESCAPE: _keyboard.escape_key,
    Keyboard.KEY_F1: _keyboard.function_keys[1],
    Keyboard.KEY_F2: _keyboard.function_keys[2],
    Keyboard.KEY_F3: _keyboard.function_keys[3],
    Keyboard.KEY_F4: _keyboard.function_keys[4],
    Keyboard.KEY_F5: _keyboard.function_keys[5],
    Keyboard.KEY_F6: _keyboard.function_keys[6],
    Keyboard.KEY_F7: _keyboard.function_keys[7],
    Keyboard.KEY_F8: _keyboard.function_keys[8],
    Keyboard.KEY_F9: _keyboard.function_keys[9],
    Keyboard.KEY_F10: _keyboard.function_keys[10],
    Keyboard.KEY_F11: _keyboard.function_keys[11],
    Keyboard.KEY_F12: _keyboard.function_keys[12],
    Keyboard.KEY_DELETE: _keyboard.delete_key,

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
    Keyboard.KEY_BACKSPACE: _keyboard.backspace_key,

    Keyboard.KEY_TAB: _keyboard.tab_key,
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

    Keyboard.KEY_CAPSLOCK: _keyboard.caps_lock_key,
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
    Keyboard.KEY_ENTER: _keyboard.enter_key,

    Keyboard.KEY_LEFT_SHIFT: _keyboard.shift_l_key,
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
    Keyboard.KEY_RIGHT_SHIFT: _keyboard.shift_r_key,

    Keyboard.KEY_LEFT_CTRL: _keyboard.control_l_key,
    Keyboard.KEY_LEFT_WINDOWS: _keyboard.windows_l_key,
    Keyboard.KEY_LEFT_ALT: _keyboard.alt_l_key,
    Keyboard.KEY_SPACE: _keyboard.space_key,
    Keyboard.KEY_RIGHT_ALT: _keyboard.alt_r_key,
    Keyboard.KEY_RIGHT_CTRL: _keyboard.control_r_key,

    Keyboard.KEY_UP: _keyboard.up_key,
    Keyboard.KEY_LEFT: _keyboard.left_key,
    Keyboard.KEY_DOWN: _keyboard.down_key,
    Keyboard.KEY_RIGHT: _keyboard.right_key,
}


class InputControllerPyuserinput(InputController):
    def __init__(self):
        pass

    def key_press(self, key):
        _keyboard.press_key(PYUSERINPUT_KEYBOARD_MAP[key])

    def key_release(self, key):
        _keyboard.release_key(PYUSERINPUT_KEYBOARD_MAP[key])

    def key_tap(self, key):
        _keyboard.tap_key(PYUSERINPUT_KEYBOARD_MAP[key])

    def mouse_press(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        _mouse.press(position[0], position[1], PYUSERINPUT_MOUSE_MAP[button])

    def mouse_release(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        _mouse.release(position[0], position[1], PYUSERINPUT_MOUSE_MAP[button])

    def mouse_click(self, button=Mouse.BUTTON_LEFT, position=(None, None)):
        _mouse.click(position[0], position[1], PYUSERINPUT_MOUSE_MAP[button])

    def mouse_move_to(self, position):
        _mouse.move(position[0], position[1])

    def mouse_scroll(self, amount, position=(None, None)):
        _mouse.move(position[0], position[1])
        _mouse.scroll(vertical=amount)

    @property
    def mouse_position(self):
        return _mouse.position()

    @property
    def screen_size(self):
        return _mouse.screen_size()
