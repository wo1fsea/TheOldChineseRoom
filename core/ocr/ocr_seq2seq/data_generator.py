# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/1/26
Description:
    data_generator.py
----------------------------------------------------------------------------"""
import numpy as np
from keras import backend as K
from .image_generator import ImageGenerator
from .utils import text_to_label


class DataGenerator(object):
    def __init__(self, image_width, image_height, output_length, minibatch_size, font_set, alphabet, word_list=[]):
        self.image_generator = ImageGenerator(image_width, image_height, font_set)
        self._image_width = image_width
        self._image_height = image_height
        self._ouput_length = output_length
        self._minibatch_size = minibatch_size
        self._alphabet = alphabet
        self._word_list = word_list

    def _get_random_string(self):
        char = []
        length = np.random.randint(1, 8)
        for i in range(length):
            c = ""
            while not c:
                c = np.random.choice(self._alphabet)
            char.append(c)
        return "".join(char)

    def _get_image(self, text):
        image = self.image_generator.generate(text, rotation=True, translate=True, noise=True)
        image = image.astype(np.float32) / 255
        return image

    def _get_batch_date(self):
        if K.image_data_format() == 'channels_first':
            X_data = np.ones([self._minibatch_size, 1, self._image_width, self._image_height])
        else:
            X_data = np.ones([self._minibatch_size, self._image_width, self._image_height, 1])

        label = np.ones([self._minibatch_size, 8])
        output_length = np.zeros([self._minibatch_size, 1])
        label_length = np.zeros([self._minibatch_size, 1])

        source_str = []
        for i in range(self._minibatch_size):
            # Mix in some blank inputs.  This seems to be important for
            # achieving translational invariance
            text = self._get_random_string()
            image = self._get_image(text)

            if K.image_data_format() == 'channels_first':
                X_data[i, 0, 0:self._image_width, :] = image[0, :, :].T
            else:
                X_data[i, 0:self._image_width, :, 0] = image[0, :, :].T

            t_label = text_to_label(text, self._alphabet)
            label[i, 0:len(t_label)] = t_label
            label_length[i] = len(t_label)
            output_length[i] = self._ouput_length
            source_str.append(text)

        inputs = {
            'image_input': X_data,
            'label': label,
            'output_length': output_length,
            'label_length': label_length,
            'source_str': source_str,
        }
        outputs = {'ctc': np.zeros([self._minibatch_size])}  # dummy data for dummy loss function
        return (inputs, outputs)

    def get_validate_data(self):
        while 1:
            yield self._get_batch_date()

    def get_train_data(self):
        while 1:
            yield self._get_batch_date()

    def get_test_date(self):
        while 1:
            yield self._get_batch_date()
