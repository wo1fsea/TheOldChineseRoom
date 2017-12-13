# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong
    gzhuangquanyong@corp.netease.com
Date:
    2017/10/13
Description:
    keys
History:
    2017/10/13, create file.
----------------------------------------------------------------------------"""


# from enum import Enum


class Mouse:
    BUTTON_LEFT = "BUTTON_LEFT",
    BUTTON_MIDDLE = "BUTTON_MIDDLE",
    BUTTON_RIGHT = "BUTTON_RIGHT",
    BUTTON_UNKNOWN = "BUTTON_UNKNOWN",


class Keyboard:
    KEY_ESCAPE = "KEY_ESCAPE"
    KEY_F1 = "KEY_F1"
    KEY_F2 = "KEY_F2"
    KEY_F3 = "KEY_F3"
    KEY_F4 = "KEY_F4"
    KEY_F5 = "KEY_F5"
    KEY_F6 = "KEY_F6"
    KEY_F7 = "KEY_F7"
    KEY_F8 = "KEY_F8"
    KEY_F9 = "KEY_F9"
    KEY_F10 = "KEY_F10"
    KEY_F11 = "KEY_F11"
    KEY_F12 = "KEY_F12"
    KEY_DELETE = "KEY_DELETE"

    KEY_GRAVE = "KEY_GRAVE"
    KEY_1 = "KEY_1"
    KEY_2 = "KEY_2"
    KEY_3 = "KEY_3"
    KEY_4 = "KEY_4"
    KEY_5 = "KEY_5"
    KEY_6 = "KEY_6"
    KEY_7 = "KEY_7"
    KEY_8 = "KEY_8"
    KEY_9 = "KEY_9"
    KEY_0 = "KEY_0"
    KEY_MINUS = "KEY_MINUS"
    KEY_EQUALS = "KEY_EQUALS"
    KEY_BACKSPACE = "KEY_BACKSPACE"

    KEY_TAB = "KEY_TAB"
    KEY_Q = "KEY_Q"
    KEY_W = "KEY_W"
    KEY_E = "KEY_E"
    KEY_R = "KEY_R"
    KEY_T = "KEY_T"
    KEY_Y = "KEY_Y"
    KEY_U = "KEY_U"
    KEY_I = "KEY_I"
    KEY_O = "KEY_O"
    KEY_P = "KEY_P"
    KEY_LEFT_BRACKET = "KEY_LEFT_BRACKET"
    KEY_RIGHT_BRACKET = "KEY_RIGHT_BRACKET"
    KEY_BACKSLASH = "KEY_BACKSLASH"

    KEY_CAPSLOCK = "KEY_CAPSLOCK"
    KEY_A = "KEY_A"
    KEY_S = "KEY_S"
    KEY_D = "KEY_D"
    KEY_F = "KEY_F"
    KEY_G = "KEY_G"
    KEY_H = "KEY_H"
    KEY_J = "KEY_J"
    KEY_K = "KEY_K"
    KEY_L = "KEY_L"
    KEY_SEMICOLON = "KEY_SEMICOLON"
    KEY_APOSTROPHE = "KEY_APOSTROPHE"
    KEY_ENTER = "KEY_ENTER"

    KEY_LEFT_SHIFT = "KEY_LEFT_SHIFT"
    KEY_Z = "KEY_Z"
    KEY_X = "KEY_X"
    KEY_C = "KEY_C"
    KEY_V = "KEY_V"
    KEY_B = "KEY_B"
    KEY_N = "KEY_N"
    KEY_M = "KEY_M"
    KEY_COMMA = "KEY_COMMA"
    KEY_PERIOD = "KEY_PERIOD"
    KEY_SLASH = "KEY_SLASH"
    KEY_RIGHT_SHIFT = "KEY_RIGHT_SHIFT"

    KEY_LEFT_CTRL = "KEY_LEFT_CTRL"
    KEY_LEFT_WINDOWS = "KEY_LEFT_WINDOWS"
    KEY_LEFT_ALT = "KEY_LEFT_ALT"
    KEY_SPACE = "KEY_SPACE"
    KEY_RIGHT_ALT = "KEY_RIGHT_ALT"
    KEY_RIGHT_CTRL = "KEY_RIGHT_CTRL"

    KEY_UP = "KEY_UP"
    KEY_LEFT = "KEY_LEFT"
    KEY_DOWN = "KEY_DOWN"
    KEY_RIGHT = "KEY_RIGHT"

    KEY_INSERT = "KEY_INSERT"
    KEY_PRINT_SCREEN = "KEY_PRINT_SCREEN"
    KEY_SCROLL_LOCK = "KEY_SCROLL_LOCK"
    KEY_PAUSE = "KEY_PAUSE"
    KEY_HOME = "KEY_HOME"
    KEY_END = "KEY_END"
    KEY_PAGE_UP = "KEY_PAGE_UP"
    KEY_PAGE_DOWN = "KEY_PAGE_DOWN"

    KEY_UNKNOWN = "KEU_UNKNOWN"


CHARACTER_KEY_MAP = {
    "`": [Keyboard.KEY_GRAVE],
    "~": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_GRAVE],
    "1": [Keyboard.KEY_1],
    "!": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_1],
    "2": [Keyboard.KEY_2],
    "@": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_2],
    "3": [Keyboard.KEY_3],
    "#": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_3],
    "4": [Keyboard.KEY_4],
    "$": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_4],
    "5": [Keyboard.KEY_5],
    "%": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_5],
    "6": [Keyboard.KEY_6],
    "^": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_6],
    "7": [Keyboard.KEY_7],
    "&": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_7],
    "8": [Keyboard.KEY_8],
    "*": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_8],
    "9": [Keyboard.KEY_9],
    "(": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_9],
    "0": [Keyboard.KEY_0],
    ")": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_0],
    "-": [Keyboard.KEY_MINUS],
    "_": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_MINUS],
    "=": [Keyboard.KEY_EQUALS],
    "+": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_EQUALS],
    "q": [Keyboard.KEY_Q],
    "Q": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_Q],
    "w": [Keyboard.KEY_W],
    "W": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_W],
    "e": [Keyboard.KEY_E],
    "E": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_E],
    "r": [Keyboard.KEY_R],
    "R": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_R],
    "t": [Keyboard.KEY_T],
    "T": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_T],
    "y": [Keyboard.KEY_Y],
    "Y": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_Y],
    "u": [Keyboard.KEY_U],
    "U": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_U],
    "i": [Keyboard.KEY_I],
    "I": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_I],
    "o": [Keyboard.KEY_O],
    "O": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_O],
    "p": [Keyboard.KEY_P],
    "P": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_P],
    "[": [Keyboard.KEY_LEFT_BRACKET],
    "{": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_LEFT_BRACKET],
    "]": [Keyboard.KEY_RIGHT_BRACKET],
    "}": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_RIGHT_BRACKET],
    "\n": [Keyboard.KEY_ENTER],
    "a": [Keyboard.KEY_A],
    "A": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_A],
    "s": [Keyboard.KEY_S],
    "S": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_S],
    "d": [Keyboard.KEY_D],
    "D": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_D],
    "f": [Keyboard.KEY_F],
    "F": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_F],
    "g": [Keyboard.KEY_G],
    "G": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_G],
    "h": [Keyboard.KEY_H],
    "H": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_H],
    "j": [Keyboard.KEY_J],
    "J": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_J],
    "k": [Keyboard.KEY_K],
    "K": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_K],
    "l": [Keyboard.KEY_L],
    "L": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_L],
    ";": [Keyboard.KEY_SEMICOLON],
    ":": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_SEMICOLON],
    "'": [Keyboard.KEY_APOSTROPHE],
    '"': [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_APOSTROPHE],
    "z": [Keyboard.KEY_Z],
    "Z": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_Z],
    "x": [Keyboard.KEY_X],
    "X": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_X],
    "c": [Keyboard.KEY_C],
    "C": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_C],
    "v": [Keyboard.KEY_V],
    "V": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_V],
    "b": [Keyboard.KEY_B],
    "B": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_B],
    "n": [Keyboard.KEY_N],
    "N": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_N],
    "m": [Keyboard.KEY_M],
    "M": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_M],
    ",": [Keyboard.KEY_COMMA],
    "<": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_COMMA],
    ".": [Keyboard.KEY_PERIOD],
    ">": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_PERIOD],
    "/": [Keyboard.KEY_SLASH],
    "?": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_SLASH],
    "\\": [Keyboard.KEY_BACKSLASH],
    "|": [Keyboard.KEY_LEFT_SHIFT, Keyboard.KEY_BACKSLASH],
    " ": [Keyboard.KEY_SPACE]
}
