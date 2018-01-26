# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/1/27
Description:
    predictor.py
----------------------------------------------------------------------------"""
import os
import itertools
import codecs
import re
import datetime
import cairocffi as cairo
import editdistance
import numpy as np
from scipy import ndimage
import pylab
from keras import backend as K
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers import Input, Dense, Activation, Permute
from keras.layers import Reshape, Lambda
from keras.layers.merge import add, concatenate, multiply
from keras.models import Model
from keras.layers.recurrent import GRU
from keras.optimizers import SGD
from keras.utils.data_utils import get_file
from keras.preprocessing import image
import keras.callbacks

CNN_FILTER_NUM = 16
words_per_epoch = 16000
val_split = 0.2
val_words = int(words_per_epoch * (val_split))

# Network parameters
conv_filters = 16
kernel_size = (4, 4)
pool_size = 2
time_dense_size = 32
rnn_size = 128
minibatch_size = 32


class Predictor(object):
    def __init__(self, image_width, image_height):
        self.image_width = image_width
        self.image_height = image_height
        self.alphabet = 0

    def _get_input_size(self):
        if K.image_data_format() == 'channels_first':
            input_shape = (1, self.image_width, self.image_height)
        else:
            input_shape = (self.image_width, self.image_height, 1)

        return input_shape

    def _init_model(self):
        act = 'relu'
        input_layer = Input(name='input_layer', shape=self._get_input_size(), dtype='float32')
        conv_layer1 = Conv2D(CNN_FILTER_NUM, kernel_size, padding='same', activation=act,
                             kernel_initializer='he_normal', name='conv_layer1')(input_layer)
        pooling_layer1 = MaxPooling2D(pool_size=(pool_size, pool_size), name='pooling_layer1')(conv_layer1)

        conv_layer2 = Conv2D(conv_filters, kernel_size, padding='same', activation=act, kernel_initializer='he_normal',
                             name='conv_layer2')(pooling_layer1)
        pooling_layer2 = MaxPooling2D(pool_size=(pool_size, pool_size), name='pooling_layer2')(conv_layer2)

        conv_to_rnn_dims = (
            self.image_width // (pool_size ** 2), (self.image_height // (pool_size ** 2)) * conv_filters)
        reshape_layer = Reshape(target_shape=conv_to_rnn_dims, name='reshape_layer')(pooling_layer2)

        full_connected_layer = Dense(time_dense_size, activation=act, name='full_connected_layer')(reshape_layer)

        # Two layers of bidirectional GRUs
        # GRU seems to work as well, if not better than LSTM:
        gru_layer1 = GRU(rnn_size, return_sequences=True, kernel_initializer='he_normal', name='gru_layer1')(
            full_connected_layer)
        gru_backwards_layer1 = GRU(rnn_size, return_sequences=True, go_backwards=True, kernel_initializer='he_normal',
                                   name='gru_backwards_layer1')(full_connected_layer)

        code = concatenate([gru_layer1, gru_backwards_layer1])
        codeT = Permute((2, 1))(code)
        attentionT = Dense(round(self.image_width / pool_size ** 2), activation='softmax')(codeT)
        attention = Permute((2, 1))(attentionT)
        code = multiply([code, attention], name='attention')

        gru_layer2 = GRU(rnn_size, return_sequences=True, kernel_initializer='he_normal', name='gru_layer2')(code)
        gru_backwards_layer2 = GRU(rnn_size, return_sequences=True, go_backwards=True, kernel_initializer='he_normal',
                                   name='gru_backwards_layer2')(code)

        # transforms RNN output to character activations:
        y_predict = Dense(len(self.alphabet) + 1, activation="softmax", kernel_initializer='he_normal', name='dense2')(
            concatenate([gru_layer2, gru_backwards_layer2]))
        # y_predict = Activation('softmax', name='softmax')(attention)

        self.model = Model(inputs=input_layer, outputs=y_predict)
        self.model.summary()

    def train(self):
        pass

    def predict(self, image):
        pass

    def load_config(self):
        pass

    def save_config(self):
        pass
