import numpy as np
import urllib.request
from asyncio import ensure_future
from bs4 import BeautifulSoup, SoupStrainer
from pulsar.api import arbiter, command, spawn, send
from pulsar.api import get_actor

from actors import homepages_from_wikicrp

WIKICFP_FILENAME = 'working_files/wikicfp_conf.txt'
CONFERENCES_HOMEPAGES_FILENAME ='working_files/conferences_homepages.txt'
FIRST_LEVEL_ACTORS = ['get_homepages_1', 'get_homepages_2', 'get_homepages_3', 'get_homepages_4', 'get_homepages_5']

def original_links():
    file = open('conferences_homepages.txt', 'r')
    lines = file.readlines()
    file.close()
    file = open('conferences_homepages.txt', 'w')
    List = list(set(lines))
    iter=0
    while iter<len(List):
        file.write(List[iter])
        iter = iter + 1
    file.close()

def file_len(fname):    # funkcja obliczania dlugosci pliku
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1



class MainArbiter:
    # Arbiter uruchamia agentow pierwszego stopnia: czytanie linkow stron konferencji na wikicfp z pliku
    # wikicfp_conf_orig.txt, na tych stronach wyszukiwanie linkow do stron konferencji i wrzucanie do pliku
    # conferences_homepages.txt. Agenci zlecają zadania dalej następnym agentom.

    def __init__(self):
        main_arbiter = arbiter()
        self._loop = main_arbiter._loop    # kod z przykladu w dokumentacji
        self._loop.call_later(1, self)
        main_arbiter.start()

    def __call__(self, a=None): # kod z przykladu w dokumentacji
        ensure_future(self._work(a))

    async def _work(self, a=None):
        indexes_pair_dict = self.prepare_indexes()
        print(indexes_pair_dict)

        #czyszczenie tekstowego pliku
        f = open(CONFERENCES_HOMEPAGES_FILENAME, 'w')
        f.close()

        spawned_actors = []
        for actor_name in FIRST_LEVEL_ACTORS:
            spawned_actors.append(spawn(name=actor_name))

        for actor in spawned_actors:
            await actor

        sent_actions = []
        for actor, actor_name in zip(spawned_actors, FIRST_LEVEL_ACTORS):
            sent_actions.append(send(actor, 'parse_homepages_from_wiki_lvl1', indexes_pair_dict[actor_name]))

        print("Awaiting")

        for action in sent_actions:
            await action

        print("CLOSING")
        for actor in spawned_actors:
            await send(actor, 'stop')

        self._loop.call_later(5, self, a)

    def prepare_indexes(self):
        wikicfp_file_length = file_len(WIKICFP_FILENAME)
        print("Number of records: " + str(wikicfp_file_length))

        actors_number = len(FIRST_LEVEL_ACTORS)
        print("Number of first level actors: " + str(actors_number))

        line_dict = {}
        indexes = self.split_to_chunks(wikicfp_file_length, len(FIRST_LEVEL_ACTORS))

        for index_pair, key in zip(indexes, FIRST_LEVEL_ACTORS):
            line_dict[key] = index_pair

        return line_dict

    def split_to_chunks(self, elems_size, splits_number):
        avg = elems_size / float(splits_number)
        out = []
        last = 0.0
        while last < elems_size:
            out.append([int(last), int(last + avg)])
            last += avg
        return out


# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    MainArbiter()
    original_links()








