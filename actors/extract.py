import numpy as np
from asyncio import ensure_future
from bs4 import BeautifulSoup, SoupStrainer
from pulsar.api import arbiter, command, spawn, send
from pulsar.api import get_actor
import pycrfsuite
from actors.utils import training_set_preparation, create_ontology


@command()
async def extract_data(request, message):
    print("EXTRACT DATA")
    X, y = training_set_preparation.prepare_training_data_from_html(message)
    tagger = pycrfsuite.Tagger()
    tagger.open("working_files/crf.model")
    y_pred = [tagger.tag(xseq) for xseq in X]

    for i in range(len(X)):
        dicct = {
            "NAME": [],
            "TIME": [],
            "PLACE": [],
            "SHORT": [],
            "DIFF": []
        }

        last = 'DIFF'
        current = []
        for pred, x in zip(y_pred[i], [x[1].split("=")[1] for x in X[i]]):
            if pred == last:
                current.append(x)
            else:
                previous_entry = dicct[last]
                if len(previous_entry) == 0:
                    previous_entry.extend(current)
                current = []
                current.append(x)
                last = pred

        dict_strings = {
            "NAME": ' '.join(dicct['NAME']),
            "TIME": ' '.join(dicct['TIME']),
            "PLACE": ' '.join(dicct['PLACE']),
            "SHORT": ' '.join(dicct['SHORT'])
        }

        print("ZNALEZIONE CIAGI: " , dict_strings)
        create_ontology.run_onto(dict_strings)
    return

