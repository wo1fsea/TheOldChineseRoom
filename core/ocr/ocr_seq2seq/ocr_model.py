# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/1/27
Description:
    ocr_model.py
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

from .data_generator import DataGenerator, label_to_text

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

ALPHABET = "1234567890-=" \
           "!@#$%^&*()_+" \
           "qwertyuiop[]\\" \
           "QWERTYUIOP{}|" \
           "asdfghjkl;'" \
           "ASDFGHJKL:\"" \
           "zxcvbnm,./" \
           "ZXCVBNM<>?"

ALPHABET_NUM = "+-1234567890.,"

FONT_SIZE = 32
FONT = "arial.ttf"


# the actual loss calc occurs here despite it not being
# an internal Keras loss function

def ctc_lambda_func(args):
    y_pred, labels, input_length, label_length = args
    # the 2 is critical here since the first couple outputs of the RNN
    # tend to be garbage:
    y_pred = y_pred[:, :, :]
    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)


# For a real OCR application, this should be beam search with a dictionary
# and language model.  For this example, best path is sufficient.

def decode_batch(test_func, word_batch):
    out = test_func([word_batch])[0]
    ret = []
    for j in range(out.shape[0]):
        out_best = list(np.argmax(out[j, 2:], 1))
        out_best = [k for k, g in itertools.groupby(out_best)]
        outstr = label_to_text(out_best)
        ret.append(outstr)
    return ret


class OCRModel(object):
    def __init__(self, image_width, image_height):
        self.image_width = image_width
        self.image_height = image_height
        self.output_length = round(image_width // pool_size ** 2)
        self.alphabet = []
        self.data_generator = DataGenerator(self.image_width, self.image_height, self.output_length, minibatch_size=256,
                                            font_set=(FONT,), alphabet=ALPHABET)

    def _get_input_size(self):
        if K.image_data_format() == 'channels_first':
            input_shape = (1, self.image_width, self.image_height)
        else:
            input_shape = (self.image_width, self.image_height, 1)

        return input_shape

    def _get_train_model(self):
        act = 'relu'
        input_data = Input(name='image_input', shape=self._get_input_size(), dtype='float32')
        inner = Conv2D(conv_filters, kernel_size, padding='same',
                       activation=act, kernel_initializer='he_normal',
                       name='conv1')(input_data)
        inner = MaxPooling2D(pool_size=(pool_size, pool_size), name='max1')(inner)
        inner = Conv2D(conv_filters, kernel_size, padding='same',
                       activation=act, kernel_initializer='he_normal',
                       name='conv2')(inner)
        inner = MaxPooling2D(pool_size=(pool_size, pool_size), name='max2')(inner)

        conv_to_rnn_dims = (
            self.image_width // (pool_size ** 2), (self.image_height // (pool_size ** 2)) * conv_filters)
        inner = Reshape(target_shape=conv_to_rnn_dims, name='reshape')(inner)

        # cuts down input size going into RNN:
        inner = Dense(time_dense_size, activation=act, name='dense1')(inner)

        # Two layers of bidirectional GRUs
        # GRU seems to work as well, if not better than LSTM:
        gru_1 = GRU(rnn_size, return_sequences=True, kernel_initializer='he_normal', name='gru1')(inner)
        gru_1b = GRU(rnn_size, return_sequences=True, go_backwards=True, kernel_initializer='he_normal', name='gru1_b')(
            inner)

        code = concatenate([gru_1, gru_1b])
        inner = Permute((2, 1))(code)
        inner = Dense(self.output_length, activation='softmax')(inner)
        attention = Permute((2, 1), name='attention_vec')(inner)
        code = multiply([code, attention], name='attention_mul')

        # gru1_merged = add([gru_1, gru_1b])
        gru_2 = GRU(rnn_size, return_sequences=True, kernel_initializer='he_normal', name='gru2')(code)
        gru_2b = GRU(rnn_size, return_sequences=True, go_backwards=True, kernel_initializer='he_normal', name='gru2_b')(
            code)

        # transforms RNN output to character activations:
        attention = Dense(1 + len(self.alphabet), kernel_initializer='he_normal', name='dense2')(
            concatenate([gru_2, gru_2b]))
        # gru_decoder = GRU(img_gen.get_output_size(), return_sequences=True, kernel_initializer='he_normal', name='gru_decoder')(attention)
        y_pred = Activation('softmax', name='softmax')(attention)

        labels = Input(name='label', shape=[8], dtype='float32')
        input_length = Input(name='output_length', shape=[1], dtype='int64')
        label_length = Input(name='label_length', shape=[1], dtype='int64')
        # Keras doesn't currently support loss funcs with extra parameters
        # so CTC loss is implemented in a lambda layer
        loss_out = Lambda(ctc_lambda_func, output_shape=(1,), name='ctc')([y_pred, labels, input_length, label_length])

        # clipnorm seems to speeds up convergence
        sgd = SGD(lr=0.02, decay=1e-6, momentum=0.9, nesterov=True, clipnorm=5)

        model = Model(inputs=[input_data, labels, input_length, label_length], outputs=loss_out)

        # the loss calc occurs elsewhere, so use a dummy lambda func for the loss
        model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=sgd)
        model.summary()

        return model

    def _get_predict_model(self):
        act = 'relu'
        input_data = Input(name='image_input', shape=input_shape, dtype='float32')
        inner = Conv2D(conv_filters, kernel_size, padding='same',
                       activation=act, kernel_initializer='he_normal',
                       name='conv1')(input_data)
        inner = MaxPooling2D(pool_size=(pool_size, pool_size), name='max1')(inner)
        inner = Conv2D(conv_filters, kernel_size, padding='same',
                       activation=act, kernel_initializer='he_normal',
                       name='conv2')(inner)
        inner = MaxPooling2D(pool_size=(pool_size, pool_size), name='max2')(inner)

        conv_to_rnn_dims = (img_w // (pool_size ** 2), (img_h // (pool_size ** 2)) * conv_filters)
        inner = Reshape(target_shape=conv_to_rnn_dims, name='reshape')(inner)

        # cuts down input size going into RNN:
        inner = Dense(time_dense_size, activation=act, name='dense1')(inner)

        # Two layers of bidirectional GRUs
        # GRU seems to work as well, if not better than LSTM:
        gru_1 = GRU(rnn_size, return_sequences=True, kernel_initializer='he_normal', name='gru1')(inner)
        gru_1b = GRU(rnn_size, return_sequences=True, go_backwards=True, kernel_initializer='he_normal', name='gru1_b')(
            inner)

        code = concatenate([gru_1, gru_1b])
        inner = Permute((2, 1))(code)
        inner = Dense(round(img_w / pool_size ** 2), activation='softmax')(inner)
        attention = Permute((2, 1), name='attention_vec')(inner)
        code = multiply([code, attention], name='attention_mul')

        # gru1_merged = add([gru_1, gru_1b])
        gru_2 = GRU(rnn_size, return_sequences=True, kernel_initializer='he_normal', name='gru2')(code)
        gru_2b = GRU(rnn_size, return_sequences=True, go_backwards=True, kernel_initializer='he_normal', name='gru2_b')(
            code)

        # transforms RNN output to character activations:
        attention = Dense(img_gen.get_output_size(), kernel_initializer='he_normal', name='dense2')(
            concatenate([gru_2, gru_2b]))
        # gru_decoder = GRU(img_gen.get_output_size(), return_sequences=True, kernel_initializer='he_normal', name='gru_decoder')(attention)
        y_pred = Activation('softmax', name='softmax')(attention)
        model = Model(inputs=input_data, outputs=y_pred)
        model.summary()
        return model

        labels = Input(name='label', shape=[img_gen.absolute_max_string_len], dtype='float32')
        input_length = Input(name='output_length', shape=[1], dtype='int64')
        label_length = Input(name='label_length', shape=[1], dtype='int64')
        # Keras doesn't currently support loss funcs with extra parameters
        # so CTC loss is implemented in a lambda layer
        loss_out = Lambda(ctc_lambda_func, output_shape=(1,), name='ctc')([y_pred, labels, input_length, label_length])

        # clipnorm seems to speeds up convergence
        sgd = SGD(lr=0.02, decay=1e-6, momentum=0.9, nesterov=True, clipnorm=5)

        model = Model(inputs=[input_data, labels, input_length, label_length], outputs=loss_out)

        # the loss calc occurs elsewhere, so use a dummy lambda func for the loss
        model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=sgd)

        return model

    def train(self, start_epoch=0, stop_epoch=10):
        self._model = self._get_train_model()
        if start_epoch > 0:
            weight_file = 'weights%02d.h5' % (start_epoch - 1)
            self._model.load_weights(weight_file)

        # captures output of softmax so we can decode the output during visualization
        # test_func = K.function([input_data], [y_pred])
        # viz_cb = VizCallback(run_name, test_func, img_gen.next_val())

        self._model.fit_generator(generator=self.data_generator.get_train_data(),
                                 steps_per_epoch=256,
                                 epochs=stop_epoch,
                                 validation_data=self.data_generator.get_validate_data(),
                                 validation_steps=32,
                                 callbacks=[],
                                 initial_epoch=start_epoch)

    def predict(self, image):
        pass

    def load_config(self):
        pass

    def save_config(self):
        pass
