# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/2/7
Description:
    utils.py
----------------------------------------------------------------------------"""

import itertools
import numpy as np


def text_to_label(text, alphabet):
    return [alphabet.index(char) for char in text]


def label_to_text(labels, alphabet):
    if isinstance(alphabet, str):
        alphabet = list(alphabet)
        alphabet.append("")

    return "".join([alphabet[c] for c in labels])


def greedy_decode(y_pred, alphabet):
    out_best = tuple(np.argmax(y_pred, 1))
    out_best = [k for k, g in itertools.groupby(out_best)]
    string = label_to_text(out_best, alphabet)
    return string
