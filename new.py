from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send
import numpy as np
import itertools
import urllib.request

def file_len(fname):    # funkcja obliczania dlugosci pliku
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


FILE_NAME_HOMEPAGES_WEB = "homepages_web.txt"
NAMES_DOWNLOAD = ['download_1', 'download_2', 'download_3', 'download_4', 'download_5'] #nazwy aktorow pobierajacyvh linki stron domowych konferencji z internetu (na poczatek z pliku homepages_web.txt)
# i zapisujacych te linki do pliku homepages.txt
# !!!!! na konsultacji prowadzacy mowil ze nie obowiazkowo musimy robic w aplikacji pobieranie linkow z internetu,
# mozemy juz miec plik ten tekstowy z tymi linkami
FILE_NAME_HOMEPAGES = "homepages.txt"

NAMES = ['reader_1', 'reader_2', 'reader_3', 'reader_4', 'reader_5']  # nazwy
# aktorów, czytających linki stron domowych z pliku homepages.txt, pobierajacych te strony i wywodzacych ich
# zawartosc do konsoli
# plik(można podać dowolne)
#FILE_NAME = "websites.txt"
FILE_NAME = "websites.txt"


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

    message_values = list(message.values()) # indeksy pol do zczytywania [[0, 4]]
    request.actor.logger.info("Message data: " + str(message_values))
    file_content = []
    with open(FILE_NAME_HOMEPAGES, "r") as f:
        for line in itertools.islice(f, int(message_values[0][0]),
                                        int(message_values[0][1])): # itertools.islice(iterable[, start], stop[, step]) - итератор, состоящий из среза.

            file_content.append(line.strip())

            #url = line.strip()
            #print("home_page=", url)  # print linka strony internetowej z listy kazdego agenta
            #html = urllib.request.urlopen(str(url)).read()  # print zawartosci strony z listy kazdego agenta
            #print("zawartosc home_page=", html)

        # print(f.read())
        # file_content = f.readlines()
    #print(" file_content =", file_content)
    request.actor.logger.info("FILE CONTENT: " + str(file_content))

    return file_content


@command()
def readfile0(request, message):

    message_values = list(message.values()) # indeksy pol do zczytywania [[0, 4]]
    request.actor.logger.info("Message data0: " + str(message_values))
    file_content = []
    with open(FILE_NAME_HOMEPAGES_WEB, "r") as f:
        for line in itertools.islice(f, int(message_values[0][0]),
                                        int(message_values[0][1])): # itertools.islice(iterable[, start], stop[, step]) - итератор, состоящий из среза.
            file_content.append(line.strip())

        # print(f.read())
        # file_content = f.readlines()
    #print(" file_content =", file_content)
    request.actor.logger.info("FILE HOMEPAGES_WEB CONTENT: " + str(file_content))

    return file_content





class Reader: # czytanie linkow stron domowych z pliku homepages.txt, pobieranie tych stron i drukowanie ich zawartosci do konsoli

    def __init__(self):
        a = arbiter()
        file_length = file_len(FILE_NAME_HOMEPAGES) - 1  # czyta ostatnie "/n", więc musimy długość pliku - 1
        #print("file_length normal = ", file_len(FILE_NAME_HOMEPAGES)) # file_length normal =  27
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
        for i in self.line_dict: # wpisujemy indeksy do slownika {'reader_2': [0, 4], 'reader_1': [5, 9], 'reader_3': [10, 14], 'reader_5': [15, 19], 'reader_4': [20, 25]}
            self.line_dict[i] = [indexes[counter], indexes[counter+1]-1]
            counter += 1

        print(self.line_dict)

        self._loop = a._loop    # kod z przykladu w dokumentacji
        self._loop.call_later(1, self)
        a.start()

    def __call__(self, a=None): # kod z przykladu w dokumentacji
        ensure_future(self._work(a))

    async def _work(self, a=None):

        if a is None:
            # a = await spawn(name='Reader')
            a = await spawn(name='reader')
        if NAMES:
            # name = NAMES.pop()
            # słownik nie może być pusty - inaczej rzuca błędem
            if (len(self.line_dict)!=0):
                name_indexes = self.line_dict.popitem() #  удаляет и возвращает пару (ключ, значение) ze slownika line_dict
                print("NAME INDEXES: " + str(name_indexes))

                name_index_dict = {name_indexes[0]: name_indexes[1]} #выводит пару ключ : значение ('reader_5', [0, 4])
                print("NAME INDEXES DICT: " + str(name_indexes))


                # print("Name po kolei: " + name)
                # print(name + " " + str(counter) + str(counter+1))
                # await send(a, 'greetme', {'name': name}) # użycie command:
                # greetme -nazwa komendy, wysyła zlecenie dla aktora a

                # aktor uzywa funkcji readfile do zczytywania z pliku przydzielonych dla niego linkow:
                # a - aktor, 'readfile' - nazwa wywolywanej funkcji, name_index_dict - parametry przekazywan do funkcji('reader_5', [0, 4])
                #await send(a, 'readfile', name_index_dict)  # uzycie command:
                result = await send(a, 'readfile', name_index_dict)
                leng = len(result)
                print("len(result): ", leng)
                for i in result:
                    print("strona domowa: ", i)
                    html = urllib.request.urlopen(str(i)).read()  # print zawartosci strony z listy kazdego agenta
                    print("zawartosc strony domowej: ", html)
                # greetme
                #  - nazwa
                # komendy, wysyla zlecenie dla aktora a

                self._loop.call_later(1, self, a)
        else:
            arbiter().stop()


# -------------------------------------------------------------------------------------------------

class Downl:    #  pobieranie linkow stron domowych konferencji z internetu (na poczatek z pliku), zapisywanie tych linkow do pliku homepages.txt
    def __init__(self):
        b = arbiter()
        file_length = file_len(FILE_NAME_HOMEPAGES_WEB)  # czyta ostatnie "/n", więc musimy długość pliku - 1    file_length normal =  27
        print("file_length normal = ", file_len(FILE_NAME_HOMEPAGES_WEB))
        print("File HOMEPAGES_WEB length: " + str(file_length))

        actors_number = len(NAMES_DOWNLOAD) # ilosc aktorow
        print("Number of arbiters b: " + str(actors_number))
        self.line_dict = dict.fromkeys(NAMES_DOWNLOAD, [None] * 2)  # słownik, przechowujący listy wskazujące na pierwszą i ostatnią linię, które aktor musi
                                                            # przeczytać z pliku

        # line_dict =  {'reader_2': [None, None], 'reader_4': [None, None], 'reader_5': [None, None], 'reader_3': [None, None], 'reader_1': [None, None]}
        # range(старт, стоп, шаг) - 0 - start, file_length - stop, actors_number - szag --> tworzy liste o zadanym kroku
        indexes = np.arange(0, file_length if file_length % actors_number == 0
                                else file_length - actors_number, actors_number)  # indexes =  [ 0  5 10 15 20]
        #print("indexes = ", indexes)
        indexes = indexes.tolist()  # zwraca liste indeksow indexes =  [0, 5, 10, 15, 20]
        indexes.append(file_length) # dadaje na koniec listy element = dlugosci listy, indexes =  [0, 5, 10, 15, 20, 26]

        # TODO: poprawić, żeby ładniej było!
        print("Indeksy: " + str(indexes))
        # counter = 0
        # for i in self.line_dict: # wpisujemy indeksy do slownika {'reader_2': [0, 4], 'reader_1': [5, 9], 'reader_3': [10, 14], 'reader_5': [15, 19], 'reader_4': [20, 25]}
        #     self.line_dict[i] = [indexes[counter], indexes[counter+1]-1]
        #     counter += 1

        print(self.line_dict)

        self._loop = b._loop
        self._loop.call_later(1, self)
        b.start()

    def __call__(self, b=None):
        ensure_future(self._work(b))

    async def _work(self, b=None):

        if b is None:
            b = await spawn(name='reader')
        if NAMES_DOWNLOAD:
            name_indexes = self.line_dict.popitem() #  удаляет и возвращает пару (ключ, значение) ze slownika line_dict
            print("NAME INDEXES: " + str(name_indexes))

            name_index_dict = {name_indexes[0]: name_indexes[1]} #выводит пару ключ : значение ('reader_5', [0, 4])
            print("NAME INDEXES DICT: " + str(name_indexes))

            result = await send(b, 'readfile0', name_index_dict)
            leng = len(result)
            print("len(result): ", leng)
            for i in result:
               print("strona domowa: ", i)
               html = urllib.request.urlopen(str(i)).read()  # print zawartosci strony z listy kazdego agenta
               print("zawartosc strony domowej: ", html)

            f = open('homepages_test.txt', 'w')
            for index in result:
                f.write(index + '\n')
            f.close()

            self._loop.call_later(1, self, b)
        else:
            arbiter().stop()



if __name__ == '__main__':
    Reader()
    Downl()