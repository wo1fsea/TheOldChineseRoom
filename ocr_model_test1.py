# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/2/4
Description:
    ocr_model_test1.py
----------------------------------------------------------------------------"""
import numpy as np
from keras import backend as K
from core.ocr.ocr_seq2seq.ocr_model import OCRModel
from PIL import Image
from core.ocr.ocr_seq2seq.utils import split_text_image, convert_image_to_input_data

ocr_m = OCRModel(128, 16)

# predict
ocr_m.load_config_for_predict_model(r"D:\GITHUB\TheChineseRoom\ocr_model\checkpoint_21")
img = Image.open("C:/Users/wo1fsea/Desktop/ScreenClip1.png")

imgs = split_text_image(img, 128/16)
input_data = []
for line in imgs:
    for img in line:
        input_data.append(convert_image_to_input_data(img, 128, 16))
        img.show()

size = len(input_data)

if K.image_data_format() == 'channels_first':
    input = np.ones([size, 1, 128, 16])
else:
    input = np.ones([size, 128, 16, 1])

for i, data in enumerate(input_data):
    input[i] = data

print(ocr_m.predict(input, size))

# train
# ocr_m.train(0, 100)