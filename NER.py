import math
import numpy as np
import pandas as pd

import hazm
import nltk

import transformers
from transformers import AutoTokenizer, AutoConfig
from transformers import TFAutoModelForTokenClassification

import os
from IPython.display import display, HTML, clear_output
from ipywidgets import widgets, Layout

import matplotlib.pyplot as plt

normalizer = hazm.Normalizer()


def cleanize(text):
    return normalizer.normalize(text)


def load_ner_model(model_name):
    """Load the model"""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = TFAutoModelForTokenClassification.from_pretrained(model_name)

        return model, tokenizer
    except:
        return [None] * 3


def NER(sequence, model, tokenizer, mode):
    output = {
        "city": [],
        "date": [],
        "time": [],
        "type": mode,
        "religious_times": [],
        "calendar_type": [],
        "event": []
    }

    sequence = cleanize(sequence)
    tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(sequence)))
    inputs = tokenizer.encode(sequence, return_tensors="tf")
    outputs = model(inputs)[0]

    B_DAT = outputs[:, :, 0][0]
    I_DAT = outputs[:, :, 7][0]
    B_TIM = outputs[:, :, 6][0]
    I_TIM = outputs[:, :, 13][0]

    B_LOC = outputs[:, :, 1][0]
    I_LOC = outputs[:, :, 8][0]
    B_ORG = outputs[:, :, 1][0]
    I_ORG = outputs[:, :, 8][0]

    location = B_LOC + B_ORG + I_LOC + I_ORG
    date_and_time = B_TIM + B_DAT + I_TIM + I_DAT

    if mode == 1:
        location -= 2
    elif mode == 2:
        possible_times = ["امساک", "اذان صبح", "طلوع آفتاب", "اذان ظهر",
                          "اذان عصر", "غروب آفتاب", "اذان مغرب", "اذان عشا", "نیمه شب شرعی"]
        keyss = [
            ["امساک"],
            ["صبح", "سحر"],
            ["طلوع"],
            ["ظهر"],
            ["عصر"],
            ["غروب", "افطار"],
            ["مغرب"],
            ["عشا"],
            ["نیمه شب"]]

        # Match keywords of each religious time to input sequence
        times = [any(key in sequence for key in keys) for keys in keyss]
        for i, time in enumerate(possible_times):
            if times[i]:
                output["religious_times"].append(time)
    elif mode == 3:
        date_and_time *= 0
    elif mode == 4:
        location *= 0

    city = ""
    for i, outp in enumerate(location):
        if outp > 2:
            city += tokens[i]+" "
        elif city:
            output["city"].append(city[:-1])

            city = ""

    if city:
        output["city"].append(city)

    return output
