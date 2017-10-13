# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong
	gzhuangquanyong@corp.netease.com
Date:
	2017/10/13
Description:
	xx
History:
	2017/10/13, create file.
----------------------------------------------------------------------------"""

from enum import Enum


class Key(Enum):
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


character_key_mapping = {
	"`": [Key.KEY_GRAVE],
	"~": [Key.KEY_LEFT_SHIFT, Key.KEY_GRAVE],
	"1": [Key.KEY_1],
	"!": [Key.KEY_LEFT_SHIFT, Key.KEY_1],
	"2": [Key.KEY_2],
	"@": [Key.KEY_LEFT_SHIFT, Key.KEY_2],
	"3": [Key.KEY_3],
	"#": [Key.KEY_LEFT_SHIFT, Key.KEY_3],
	"4": [Key.KEY_4],
	"$": [Key.KEY_LEFT_SHIFT, Key.KEY_4],
	"5": [Key.KEY_5],
	"%": [Key.KEY_LEFT_SHIFT, Key.KEY_5],
	"6": [Key.KEY_6],
	"^": [Key.KEY_LEFT_SHIFT, Key.KEY_6],
	"7": [Key.KEY_7],
	"&": [Key.KEY_LEFT_SHIFT, Key.KEY_7],
	"8": [Key.KEY_8],
	"*": [Key.KEY_LEFT_SHIFT, Key.KEY_8],
	"9": [Key.KEY_9],
	"(": [Key.KEY_LEFT_SHIFT, Key.KEY_9],
	"0": [Key.KEY_0],
	")": [Key.KEY_LEFT_SHIFT, Key.KEY_0],
	"-": [Key.KEY_MINUS],
	"_": [Key.KEY_LEFT_SHIFT, Key.KEY_MINUS],
	"=": [Key.KEY_EQUALS],
	"+": [Key.KEY_LEFT_SHIFT, Key.KEY_EQUALS],
	"q": [Key.KEY_Q],
	"Q": [Key.KEY_LEFT_SHIFT, Key.KEY_Q],
	"w": [Key.KEY_W],
	"W": [Key.KEY_LEFT_SHIFT, Key.KEY_W],
	"e": [Key.KEY_E],
	"E": [Key.KEY_LEFT_SHIFT, Key.KEY_E],
	"r": [Key.KEY_R],
	"R": [Key.KEY_LEFT_SHIFT, Key.KEY_R],
	"t": [Key.KEY_T],
	"T": [Key.KEY_LEFT_SHIFT, Key.KEY_T],
	"y": [Key.KEY_Y],
	"Y": [Key.KEY_LEFT_SHIFT, Key.KEY_Y],
	"u": [Key.KEY_U],
	"U": [Key.KEY_LEFT_SHIFT, Key.KEY_U],
	"i": [Key.KEY_I],
	"I": [Key.KEY_LEFT_SHIFT, Key.KEY_I],
	"o": [Key.KEY_O],
	"O": [Key.KEY_LEFT_SHIFT, Key.KEY_O],
	"p": [Key.KEY_P],
	"P": [Key.KEY_LEFT_SHIFT, Key.KEY_P],
	"[": [Key.KEY_LEFT_BRACKET],
	"{": [Key.KEY_LEFT_SHIFT, Key.KEY_LEFT_BRACKET],
	"]": [Key.KEY_RIGHT_BRACKET],
	"}": [Key.KEY_LEFT_SHIFT, Key.KEY_RIGHT_BRACKET],
	"\n": [Key.KEY_RETURN],
	"a": [Key.KEY_A],
	"A": [Key.KEY_LEFT_SHIFT, Key.KEY_A],
	"s": [Key.KEY_S],
	"S": [Key.KEY_LEFT_SHIFT, Key.KEY_S],
	"d": [Key.KEY_D],
	"D": [Key.KEY_LEFT_SHIFT, Key.KEY_D],
	"f": [Key.KEY_F],
	"F": [Key.KEY_LEFT_SHIFT, Key.KEY_F],
	"g": [Key.KEY_G],
	"G": [Key.KEY_LEFT_SHIFT, Key.KEY_G],
	"h": [Key.KEY_H],
	"H": [Key.KEY_LEFT_SHIFT, Key.KEY_H],
	"j": [Key.KEY_J],
	"J": [Key.KEY_LEFT_SHIFT, Key.KEY_J],
	"k": [Key.KEY_K],
	"K": [Key.KEY_LEFT_SHIFT, Key.KEY_K],
	"l": [Key.KEY_L],
	"L": [Key.KEY_LEFT_SHIFT, Key.KEY_L],
	";": [Key.KEY_SEMICOLON],
	":": [Key.KEY_LEFT_SHIFT, Key.KEY_SEMICOLON],
	"'": [Key.KEY_APOSTROPHE],
	'"': [Key.KEY_LEFT_SHIFT, Key.KEY_APOSTROPHE],
	"z": [Key.KEY_Z],
	"Z": [Key.KEY_LEFT_SHIFT, Key.KEY_Z],
	"x": [Key.KEY_X],
	"X": [Key.KEY_LEFT_SHIFT, Key.KEY_X],
	"c": [Key.KEY_C],
	"C": [Key.KEY_LEFT_SHIFT, Key.KEY_C],
	"v": [Key.KEY_V],
	"V": [Key.KEY_LEFT_SHIFT, Key.KEY_V],
	"b": [Key.KEY_B],
	"B": [Key.KEY_LEFT_SHIFT, Key.KEY_B],
	"n": [Key.KEY_N],
	"N": [Key.KEY_LEFT_SHIFT, Key.KEY_N],
	"m": [Key.KEY_M],
	"M": [Key.KEY_LEFT_SHIFT, Key.KEY_M],
	",": [Key.KEY_COMMA],
	"<": [Key.KEY_LEFT_SHIFT, Key.KEY_COMMA],
	".": [Key.KEY_PERIOD],
	">": [Key.KEY_LEFT_SHIFT, Key.KEY_PERIOD],
	"/": [Key.KEY_SLASH],
	"?": [Key.KEY_LEFT_SHIFT, Key.KEY_SLASH],
	"\\": [Key.KEY_BACKSLASH],
	"|": [Key.KEY_LEFT_SHIFT, Key.KEY_BACKSLASH],
	" ": [Key.KEY_SPACE]
}
