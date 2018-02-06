# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong
	gzhuangquanyong@corp.netease.com
Date:
	2018/2/6
Description:
	utils
----------------------------------------------------------------------------"""


def text_to_label(text, alphabet):
	return [alphabet.index(char) for char in text]


def label_to_text(labels, alphabet):
	if isinstance(alphabet, str):
		alphabet = list(alphabet)
		alphabet.append("")

	return "".join([alphabet[c] for c in labels])
