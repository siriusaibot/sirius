from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf

import math
import numpy as np
import pandas as pd

import hazm
import nltk

import transformers
from transformers import AutoTokenizer, AutoConfig
from transformers import TFAutoModelForTokenClassification

from BertBasedIntent import IntentClassifier
from CityTranslate import translate
from NER import load_ner_model, NER
from ReligiousAPI import ReligiousAPI
from TimeAPI import TimeAPI
from Utils import date_to_event, event_to_date
from WeatherAPI import WeatherAPI

print()
print('tensorflow', tf.__version__, sep="\t")
print('transformers', transformers.__version__, sep="\t")
print('numpy   ', np.__version__, sep="\t")
print('pandas  ', pd.__version__, sep="\t")
print()


class BOT():
    def __init__(self):
        print("Loading Intent model...")
        self.intent_model = IntentClassifier().classify

        print("Loading NER model...")
        if tf.test.gpu_device_name() != '/device:GPU:0':
            print('GPU not found, using CPU...')
        else:
            print('Found GPU: {}'.format(tf.test.gpu_device_name()))
        model_name = 'HooshvareLab/bert-base-parsbert-peymaner-uncased'
        self.ner_model, self.ner_tokenizer = load_ner_model(model_name)

    def AIBOT(self, question):
        output = {}
        output["type"] = self.intent_model(question)

        output = NER(question, self.ner_model, self.ner_tokenizer, mode=output["type"])

        output["type"] = str(output["type"])

        return output
