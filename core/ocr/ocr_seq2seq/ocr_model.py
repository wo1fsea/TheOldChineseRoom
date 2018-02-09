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
import editdistance
import numpy as np
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

from .data_generator import DataGenerator
from .alphabet import ALPHABET_KEYBOARD
from .utils import label_to_text, greedy_decode

CNN_FILTER_NUM = 16
KERNEL_SIZE = (4, 4)
POOL_SIZE = 2
RNN_DENSE_SIZE = 32
RNN_SIZE = 128
MINIBATCH_SIZE = 256

FONT_SET = ("arial.ttf", "times.ttf", "LSANS.TTF")


# the actual loss calc occurs here despite it not being
# an internal Keras loss function

def ctc_lambda_func(args):
    y_pred, labels, input_length, label_length = args
    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)


class TrainingCallback(keras.callbacks.Callback):

    def __init__(self, test_func, test_data_gen, output_path="ocr_model", num_display_words=16):
        super(TrainingCallback, self).__init__()
        self.test_func = test_func
        self.output_path = output_path
        self.test_data_gen = test_data_gen
        self.num_display_words = num_display_words
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def show_edit_distance(self, num):
        num_left = num
        mean_norm_ed = 0.0
        mean_ed = 0.0
        while num_left > 0:
            word_batch = next(self.test_data_gen)[0]
            num_proc = min(word_batch['image_input'].shape[0], num_left)
            decoded_res = decode_batch(self.test_func, word_batch['image_input'][0:num_proc])
            for j in range(num_proc):
                edit_dist = editdistance.eval(decoded_res[j], word_batch['source_str'][j])
                mean_ed += float(edit_dist)
                mean_norm_ed += float(edit_dist) / len(word_batch['source_str'][j])
            num_left -= num_proc
        mean_norm_ed = mean_norm_ed / num
        mean_ed = mean_ed / num
        print('\nOut of %d samples:  Mean edit distance: %.3f Mean normalized edit distance: %0.3f'
              % (num, mean_ed, mean_norm_ed))

    def _visual_test(self, epoch):
        self.show_edit_distance(256)
        word_batch = next(self.test_data_gen)[0]
        res = decode_batch(self.test_func, word_batch['image_input'][0:self.num_display_words])
        if word_batch['image_input'][0].shape[0] < 256:
            cols = 2
        else:
            cols = 1
        for i in range(self.num_display_words):
            pylab.subplot(self.num_display_words // cols, cols, i + 1)
            if K.image_data_format() == 'channels_first':
                the_input = word_batch['image_input'][i, 0, :, :]
            else:
                the_input = word_batch['image_input'][i, :, :, 0]
            pylab.imshow(the_input.T, cmap='Greys_r')
            pylab.xlabel('Truth = \'%s\'\nDecoded = \'%s\'' % (word_batch['source_str'][i], res[i]))
        fig = pylab.gcf()
        fig.set_size_inches(16, 32)
        pylab.savefig(os.path.join(self.output_path, 'e%02d.png' % (epoch)))
        pylab.close()

    def on_epoch_end(self, epoch, logs={}):
        self._visual_test(epoch)


# For a real OCR application, this should be beam search with a dictionary
# and language model.  For this example, best path is sufficient.

def decode_batch(test_func, word_batch):
    out = test_func([word_batch])[0]
    ret = []
    for j in range(out.shape[0]):
        out_best = list(np.argmax(out[j], 1))
        out_best = [k for k, g in itertools.groupby(out_best)]
        outstr = label_to_text(out_best, ALPHABET_KEYBOARD)
        ret.append(outstr)
    return ret


class CheckpointSaver(keras.callbacks.Callback):
    CHECKPOINT_FILE = "checkpoint_%d"

    def __init__(self, checkpoint_path):
        super(CheckpointSaver, self).__init__()
        self._path = checkpoint_path

    def save_checkpoint(self, model, epoch):
        model.save_weights(os.path.join(self._path, self.CHECKPOINT_FILE % epoch))

    def load_checkpoint(self, model, epoch):
        model.load_weights(os.path.join(self._path, self.CHECKPOINT_FILE % epoch))

    def _checkpoint(self, epoch):
        self.save_checkpoint(self.model, epoch)

    def on_epoch_end(self, epoch, logs={}):
        self._checkpoint(epoch)


class OCRModel(object):

    def __init__(self, image_width, image_height):
        self._train_model = None
        self._predict_model = None
        self._test_func = None

        self.image_width = image_width
        self.image_height = image_height
        self.output_length = round(image_width // POOL_SIZE ** 2)
        self.alphabet = ALPHABET_KEYBOARD
        self.data_generator = DataGenerator(self.image_width, self.image_height, self.output_length, minibatch_size=MINIBATCH_SIZE,
                                            font_set=FONT_SET, alphabet=self.alphabet)

        self._init_model()

    def _get_input_size(self):
        if K.image_data_format() == 'channels_first':
            input_shape = (1, self.image_width, self.image_height)
        else:
            input_shape = (self.image_width, self.image_height, 1)

        return input_shape

    def _init_model(self):
        act = 'relu'
        input_data = Input(name='image_input', shape=self._get_input_size(), dtype='float32')
        inner = Conv2D(CNN_FILTER_NUM, KERNEL_SIZE, padding='same',
                       activation=act, kernel_initializer='he_normal',
                       name='conv1')(input_data)
        inner = MaxPooling2D(pool_size=(POOL_SIZE, POOL_SIZE), name='max1')(inner)
        inner = Conv2D(CNN_FILTER_NUM, KERNEL_SIZE, padding='same',
                       activation=act, kernel_initializer='he_normal',
                       name='conv2')(inner)
        inner = MaxPooling2D(pool_size=(POOL_SIZE, POOL_SIZE), name='max2')(inner)

        conv_to_rnn_dims = (
            self.image_width // (POOL_SIZE ** 2), (self.image_height // (POOL_SIZE ** 2)) * CNN_FILTER_NUM)
        inner = Reshape(target_shape=conv_to_rnn_dims, name='reshape')(inner)

        # cuts down input size going into RNN:
        inner = Dense(RNN_DENSE_SIZE, activation=act, name='dense1')(inner)

        # Two layers of bidirectional GRUs
        # GRU seems to work as well, if not better than LSTM:
        gru_1 = GRU(RNN_SIZE, return_sequences=True, kernel_initializer='he_normal', name='gru1')(inner)
        gru_1b = GRU(RNN_SIZE, return_sequences=True, go_backwards=True, kernel_initializer='he_normal', name='gru1_b')(
            inner)

        code = concatenate([gru_1, gru_1b])
        inner = Permute((2, 1))(code)
        inner = Dense(self.output_length, activation='softmax')(inner)
        attention = Permute((2, 1), name='attention_vec')(inner)
        code = multiply([code, attention], name='attention_mul')

        # gru1_merged = add([gru_1, gru_1b])
        gru_2 = GRU(RNN_SIZE, return_sequences=True, kernel_initializer='he_normal', name='gru2')(code)
        gru_2b = GRU(RNN_SIZE, return_sequences=True, go_backwards=True, kernel_initializer='he_normal', name='gru2_b')(
            code)

        # transforms RNN output to character activations:
        attention = Dense(len(self.alphabet), kernel_initializer='he_normal', name='dense2')(concatenate([gru_1, gru_1b]))
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

        self._predict_model = Model(inputs=input_data, outputs=y_pred)
        self._train_model = Model(inputs=[input_data, labels, input_length, label_length], outputs=loss_out)
        # the loss calc occurs elsewhere, so use a dummy lambda func for the loss
        self._train_model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=sgd)
        self._train_model.summary()
        self._test_func = K.function([input_data], [y_pred])

    def train(self, start_epoch=0, stop_epoch=10):
        checkpoint_saver = CheckpointSaver("ocr_model")

        if start_epoch > 0:
            checkpoint_saver.load_checkpoint(self._train_model, start_epoch - 1)

        # captures output of softmax so we can decode the output during visualization
        training_cb = TrainingCallback(self._test_func, self.data_generator.get_validate_data())

        self._train_model.fit_generator(generator=self.data_generator.get_train_data(),
                                        steps_per_epoch=256,
                                        epochs=stop_epoch,
                                        validation_data=self.data_generator.get_validate_data(),
                                        validation_steps=32,
                                        callbacks=[checkpoint_saver, training_cb],
                                        initial_epoch=start_epoch)

    def predict(self, images, size):
        texts = []
        labels = self._predict_model.predict([images], batch_size=size)
        l, g = K.ctc_decode(labels, np.ones((labels.shape[0],)) * self.output_length, greedy=False)
        for label in K.eval(l[0]):
            print(label_to_text(label, self.alphabet))
        for label in labels:
            texts.append(greedy_decode(label, self.alphabet))
        return texts

    def load_config_for_predict_model(self, config_file):
        self._predict_model.load_weights(config_file)

    def save_config_from_train_model(self, config_file):
        self._train_model.save_weights(config_file)
