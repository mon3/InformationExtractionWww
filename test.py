from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send
import numpy as np


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


names = ['john', 'luca', 'carl', 'jo', 'alex']
FILE_NAME = "websites.txt"


@command()
def greetme(request, message):
    echo = 'Hello {}!'.format(message['name'])
    request.actor.logger.info(echo)
    return echo


@command()
def readfile(request, message):
    # print("Entering read_file...")
    # indexes = message['name']
    print("indexes u aktora: " + str(message))
    with open(FILE_NAME, "rb") as f:
        # print(f.read())
        echo = f.readlines()
    request.actor.logger.info(echo[message])
    return echo


class Greeter:

    def __init__(self):
        a = arbiter()
        file_length = file_len(FILE_NAME)
        print("File length: " + str(file_length))
        actors_number = len(names)
        print("Number of arbiters: " + str(actors_number))
        self.line_dict = dict.fromkeys(names, [None] * 2) # słownik,
        # przechowujący
        # listy
        # wskazujące na pierwszą i ostatnią linię, które aktor musi
        # przeczytać z pliku

        indexes = np.arange(0, file_length if file_length % actors_number == 0
                                else file_length - actors_number, actors_number)
        indexes = indexes.tolist()
        indexes.append(file_length)

        # TODO: poprawić, żeby ładniej było!
        print("Indeksy: " + str(indexes))
        counter = 0
        for i in self.line_dict:
            self.line_dict[i] = [counter, counter+1]
            counter += 1

        print(self.line_dict)

        self._loop = a._loop
        self._loop.call_later(1, self)
        a.start()

    def __call__(self, a=None):
        ensure_future(self._work(a))

    async def _work(self, a=None):

        if a is None:
            # a = await spawn(name='greeter')
            a = await spawn(name='reader')
        if names:
            name = names.pop()
            name_indexes = self.line_dict.popitem()
            print("NAME INDEXES: " + str(name_indexes))

            name_index_dict = {name_indexes[0] : name_indexes[1]}
            print("NAME INDEXES DICT: " + str(name_indexes))



            # print("Name po kolei: " + name)
            # print(name + " " + str(counter) + str(counter+1))
            # await send(a, 'greetme', {'name': name}) #uzycie command:
            # greetme -nazwa komendy, wysyla zlecenie dla aktora a

            await send(a, 'readfile', name_index_dict) # uzycie command: greetme
            #  - nazwa
            # komendy, wysyla zlecenie dla aktora a

            self._loop.call_later(1, self, a)
        else:
            arbiter().stop()


if __name__ == '__main__':
    Greeter()