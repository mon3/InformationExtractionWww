from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send
import numpy as np
import itertools
import urllib.request

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


NAMES = ['reader_1', 'reader_2', 'reader_3', 'reader_4', 'reader_5']  # nazwy
# aktorów,
# pobierajacyvh strony internetowe
# można podać dowolne)
#FILE_NAME = "websites.txt"

FILE_NAME = "websites.txt"

NAMES_download = ['download_1', 'download_2']
FILE_NAME_homepages = "homepages.txt"


# komenda do testowania komunikacji pomiędzy aktorami
@command()
def greetme(request, message):
    file_content = 'Hello {}!'.format(message['name'])
    request.actor.logger.info(file_content)
    return file_content


@command()
def readfile(request, message):
    # print("Entering read_file...")
    # indexes = message['name']
    # print("indexes u aktora: " + str(message))

    message_values = list(message.values())
    request.actor.logger.info("Message data: " + str(message_values))
    file_content = []
    with open(FILE_NAME, "r") as f:
        for line in itertools.islice(f, int(message_values[0][0]),
                                        int(message_values[0][1])):

            file_content.append(line.strip())
        # print(f.read())
        # file_content = f.readlines()
    request.actor.logger.info("FILE CONTENT: " + str(file_content))
    #url = file_content
    #print("home_page=", url[0])  # print linka pierwszej strony z listy kazdego agenta
    #html = urllib.request.urlopen(str(url[0])).read() # print zawartosci pierwszej strony z listy kazdego agenta
    #print(html)

    return file_content


class Reader:

    def __init__(self):
        a = arbiter()
        file_length = file_len(FILE_NAME) - 1  # czyta ostatnie "/n", więc musimy długość pliku - 1
        # print("file_length normal = ", file_len(FILE_NAME)) # file_length normal =  27
        print("File length: " + str(file_length))

        actors_number = len(NAMES) # ilosc aktorow
        print("Number of arbiters: " + str(actors_number))
        self.line_dict = dict.fromkeys(NAMES, [None] * 2)  # słownik, przechowujący listy wskazujące na pierwszą i ostatnią linię, które aktor musi
                                                            # przeczytać z pliku

        # print("line_dict = ", self.line_dict) # line_dict =  {'reader_2': [None, None], 'reader_4': [None, None], 'reader_5': [None, None], 'reader_3': [None, None], 'reader_1': [None, None]}
        # range(старт, стоп, шаг) - 0 - start, file_length - stop, actors_number - szag --> tworzy liste o zadanym kroku
        indexes = np.arange(0, file_length if file_length % actors_number == 0
                                else file_length - actors_number, actors_number)  # indexes =  [ 0  5 10 15 20]
        #print("indexes = ", indexes)
        indexes = indexes.tolist()  # zwraca liste indeksow indexes =  [0, 5, 10, 15, 20]
        indexes.append(file_length) # dadaje na koniec listy element=dlugosci listy, indexes =  [0, 5, 10, 15, 20, 26]

        # TODO: poprawić, żeby ładniej było!
        print("Indeksy: " + str(indexes))
        counter = 0
        for i in self.line_dict:
            self.line_dict[i] = [indexes[counter], indexes[counter+1]-1]
            counter += 1

        print(self.line_dict)

        self._loop = a._loop
        self._loop.call_later(1, self)
        a.start()

    def __call__(self, a=None):
        ensure_future(self._work(a))

    async def _work(self, a=None):

        if a is None:
            # a = await spawn(name='Reader')
            a = await spawn(name='reader')
        if NAMES:
            # name = NAMES.pop()
            name_indexes = self.line_dict.popitem()
            print("NAME INDEXES: " + str(name_indexes))

            name_index_dict = {name_indexes[0]: name_indexes[1]}
            print("NAME INDEXES DICT: " + str(name_indexes))


            # print("Name po kolei: " + name)
            # print(name + " " + str(counter) + str(counter+1))
            # await send(a, 'greetme', {'name': name}) # użycie command:
            # greetme -nazwa komendy, wysyła zlecenie dla aktora a

            await send(a, 'readfile', name_index_dict)  # uzycie command:
            # greetme
            #  - nazwa
            # komendy, wysyla zlecenie dla aktora a

            self._loop.call_later(1, self, a)
        else:
            arbiter().stop()

class Downl:
    def __init__(self):
        b = arbiter()

        self._loop = b._loop
        self._loop.call_later(1, self)
        b.start()


if __name__ == '__main__':
    Reader()
