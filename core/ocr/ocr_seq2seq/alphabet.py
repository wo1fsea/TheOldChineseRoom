# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong
	gzhuangquanyong@corp.netease.com
Date:
	2018/2/6
Description:
	alphabet
----------------------------------------------------------------------------"""


def alphabet_str2tuple(alphabet):
	alphabet = list(alphabet)
	alphabet.append("")
	return tuple(alphabet)


ALPHABET_KEYBOARD = alphabet_str2tuple("1234567890-=" \
                                       "!@#$%^&*()_+" \
                                       "qwertyuiop[]\\" \
                                       "QWERTYUIOP{}|" \
                                       "asdfghjkl;'" \
                                       "ASDFGHJKL:\"" \
                                       "zxcvbnm,./" \
                                       "ZXCVBNM<>?")

ALPHABET_LOW_CASE_LETTER = alphabet_str2tuple('abcdefghijklmnopqrstuvwxyz ')
ALPHABET_CAPITAL_LETTER = alphabet_str2tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ ')
ALPHABET_NUM = alphabet_str2tuple("+-1234567890.,")
