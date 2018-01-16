import training_set_preparation
from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send
from pulsar.api import get_actor
import numpy as np
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
from actors import extract

@command()
async def extract_data(request, message):

    http_texts = message
    X, y = training_set_preparation.prepare_training_data_from_html(http_texts)

    tagger = pycrfsuite.Tagger()
    tagger.open(args.model_name)
    y_pred = [tagger.tag(xseq) for xseq in X]
    i = 0
    for x, y in zip(y_pred[i], [x[1].split("=")[1] for x in X[i]]):
        if x != 'DIFF':
            print("%s (%s)" % (y, x))
