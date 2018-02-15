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
import editdistance
import pylab
from keras import backend as K
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers import Input, Dense, Activation, Permute
from keras.layers import Reshape, Lambda
from keras.layers.merge import concatenate, multiply
from keras.models import Model
from keras.layers.recurrent import GRU, LSTM
from keras.optimizers import SGD
import keras.callbacks

from .data_generator import DataGenerator, MAX_STRING_LEN
from .alphabet import ALPHABET_KEYBOARD as ALPHABET
from .utils import label_to_text, ctc_decode, convert_input_data_to_image_array, get_input_data_shape

CNN_FILTER_NUM = 16
KERNEL_SIZE = (4, 4)
POOL_SIZE = 2
RNN_DENSE_SIZE = 32
RNN_SIZE = 128
MINIBATCH_SIZE = 256

FONT_SET = ("arial.ttf", ) #, "times.ttf", "LSANS.TTF")


def ctc_lambda_func(args):
    y_pred, labels, input_length, label_length = args
    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)


class TrainingCallback(keras.callbacks.Callback):

    def __init__(self, test_func, test_data_gen, alphabet, output_path="ocr_model", num_display_words=16):
        super(TrainingCallback, self).__init__()
        self.test_func = test_func
        self.test_data_gen = test_data_gen
        self.alphabet = alphabet
        self.output_path = output_path
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
            y_preds = self.test_func([word_batch['image_input'][0:num_proc]])[0]
            decoded_res = [label_to_text(label, self.alphabet) for label in ctc_decode(y_preds)]
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
        y_preds = self.test_func([word_batch['image_input'][0:self.num_display_words]])[0]
        res = [label_to_text(label, self.alphabet) for label in ctc_decode(y_preds)]
        for i in range(self.num_display_words):
            pylab.subplot(self.num_display_words // 2, 2, i + 1)
            pylab.imshow(convert_input_data_to_image_array(word_batch['image_input'][i]), cmap='gray')
            truth = word_batch['source_str'][i].replace("$", "\\$")
            pred = res[i].replace("$", "\\$")
            pylab.xlabel('Truth = \'%s\'\nDecoded = \'%s\'' % (truth, pred))
        fig = pylab.gcf()
        fig.set_size_inches(16, 32)
        pylab.savefig(os.path.join(self.output_path, 'e%02d.png' % (epoch)))
        pylab.close()

    def on_epoch_end(self, epoch, logs={}):
        self._visual_test(epoch)


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

    def __init__(self, image_width, image_height, alphabet=ALPHABET, font_set=FONT_SET, minibatch_size=MINIBATCH_SIZE):
        self._train_model = None
        self._predict_model = None
        self._test_func = None

        self._image_width = image_width
        self._image_height = image_height
        self._output_length = round(image_width // POOL_SIZE ** 2)
        self._alphabet = alphabet
        self._font_set = font_set
        self._minibatch_size = minibatch_size
        self.data_generator = DataGenerator(image_width=self._image_width, image_height=self._image_height,
                                            output_length=self._output_length,
                                            minibatch_size=self._minibatch_size,
                                            font_set=self._font_set,
                                            alphabet=self._alphabet)

        self._init_model()

    def _init_attention_model(self):
        act = 'relu'
        input_data_shape = get_input_data_shape(self._image_width, self._image_height, 1)
        input_data = Input(name='image_input', shape=input_data_shape, dtype='float32')

        # CNN1
        inner = Conv2D(CNN_FILTER_NUM, KERNEL_SIZE, padding='same',
                       activation=act, kernel_initializer='he_normal',
                       name='conv1')(input_data)
        inner = MaxPooling2D(pool_size=(POOL_SIZE, POOL_SIZE), name='max1')(inner)

        # CNN2
        inner = Conv2D(CNN_FILTER_NUM, KERNEL_SIZE, padding='same',
                       activation=act, kernel_initializer='he_normal',
                       name='conv2')(inner)
        inner = MaxPooling2D(pool_size=(POOL_SIZE, POOL_SIZE), name='max2')(inner)

        conv_to_rnn_dims = (
            self._image_width // (POOL_SIZE ** 2), (self._image_height // (POOL_SIZE ** 2)) * CNN_FILTER_NUM)
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
        inner = Dense(self._output_length, activation='softmax')(inner)
        attention = Permute((2, 1), name='attention_vec')(inner)
        code = multiply([code, attention], name='attention_mul')

        # gru1_merged = add([gru_1, gru_1b])
        gru_2 = GRU(RNN_SIZE, return_sequences=True, kernel_initializer='he_normal', name='gru2')(code)
        gru_2b = GRU(RNN_SIZE, return_sequences=True, go_backwards=True, kernel_initializer='he_normal', name='gru2_b')(
            code)

        # transforms RNN output to character activations:
        attention = Dense(len(self._alphabet), kernel_initializer='he_normal', name='dense2')(
            concatenate([gru_2, gru_2b]))
        # gru_decoder = GRU(img_gen.get_output_size(), return_sequences=True, kernel_initializer='he_normal', name='gru_decoder')(attention)
        y_pred = Activation('softmax', name='softmax')(attention)

        labels = Input(name='label', shape=[MAX_STRING_LEN], dtype='float32')
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

    def _init_model(self):
        act = 'relu'
        input_data_shape = get_input_data_shape(self._image_width, self._image_height, 1)
        input_data = Input(name='image_input', shape=input_data_shape, dtype='float32')
        inner = Conv2D(CNN_FILTER_NUM, KERNEL_SIZE, padding='same',
                       activation=act, kernel_initializer='he_normal',
                       name='conv1')(input_data)
        inner = MaxPooling2D(pool_size=(POOL_SIZE, POOL_SIZE), name='max1')(inner)
        inner = Conv2D(CNN_FILTER_NUM, KERNEL_SIZE, padding='same',
                       activation=act, kernel_initializer='he_normal',
                       name='conv2')(inner)
        inner = MaxPooling2D(pool_size=(POOL_SIZE, POOL_SIZE), name='max2')(inner)

        conv_to_rnn_dims = (
            self._image_width // (POOL_SIZE ** 2), (self._image_height // (POOL_SIZE ** 2)) * CNN_FILTER_NUM)
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
        inner = Dense(self._output_length, activation='softmax')(inner)
        attention = Permute((2, 1), name='attention_vec')(inner)
        code = multiply([code, attention], name='attention_mul')

        # gru1_merged = add([gru_1, gru_1b])
        gru_2 = GRU(RNN_SIZE, return_sequences=True, kernel_initializer='he_normal', name='gru2')(code)
        gru_2b = GRU(RNN_SIZE, return_sequences=True, go_backwards=True, kernel_initializer='he_normal', name='gru2_b')(
            code)

        # transforms RNN output to character activations:
        attention = Dense(len(self._alphabet), kernel_initializer='he_normal', name='dense2')(
            concatenate([gru_1, gru_1b]))
        # gru_decoder = GRU(img_gen.get_output_size(), return_sequences=True, kernel_initializer='he_normal', name='gru_decoder')(attention)
        y_pred = Activation('softmax', name='softmax')(attention)

        labels = Input(name='label', shape=[MAX_STRING_LEN], dtype='float32')
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

        training_cb = TrainingCallback(self._test_func, self.data_generator.get_validate_data(), self._alphabet)

        self._train_model.fit_generator(generator=self.data_generator.get_train_data(),
                                        steps_per_epoch=256,
                                        epochs=stop_epoch,
                                        validation_data=self.data_generator.get_validate_data(),
                                        validation_steps=32,
                                        callbacks=[checkpoint_saver, training_cb],
                                        initial_epoch=start_epoch)

    def predict(self, input_data_batch):
        texts = []
        y_preds = self._predict_model.predict([input_data_batch], batch_size=input_data_batch.shape[0])
        labels = ctc_decode(y_preds)
        for label in labels:
            texts.append(label_to_text(label, self._alphabet))
        return texts

    def load_config_for_predict_model(self, config_file):
        self._predict_model.load_weights(config_file)

    def save_config_from_train_model(self, config_file):
        self._train_model.save_weights(config_file)
