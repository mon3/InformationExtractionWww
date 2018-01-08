from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send
import numpy as np
import itertools
import urllib.request
import requests
from bs4 import BeautifulSoup, SoupStrainer


# wyszukiwanie i pobieranie linkow ze strony http://www.wikicfp.com/cfp/allcfp?page= na podstrony wikicfp do poszczegolnych
# konferencji i zapisywanie ich do pliku wikicfp_conf.txt
def wikicfp_link(number, n2):
    link='http://www.wikicfp.com/cfp/allcfp?page='
    ind=1
    f = open('wikicfp_conf.txt', 'w')
    #while ind <= number:
    #while number!=0:
    while number >= n2:
        html = urllib.request.urlopen(link + str(number))
        #html = urllib.request.urlopen(link + str(ind))
        soup = BeautifulSoup(html, 'html.parser').find('div', class_='contsec')
        count=0
        for i in soup.find_all('a', href=True):
            count=count+1
            if count<=20: # na kazdej stronie jest 20 linkow na konferencje
                f.write("http://www.wikicfp.com" +i['href'] + '\n')
                print("http://www.wikicfp.com" +i['href'])
        number=number-1
    f.close()

def file_len(fname):    # funkcja obliczania dlugosci pliku
    with open(fname) as f:
        for i, l in enumerate(f):
            #print("i=", i)
            pass
    return i + 1

#print("Dlugosc pliku conf.txt:", file_len('conf.txt'))

FILE_NAME_HOMEPAGES = "wikicfp_conf.txt"

NAMES = ['reader_1', 'reader_2', 'reader_3']
#NAMES = ['reader_1', 'reader_2', 'reader_3', 'reader_4', 'reader_5']
# nazwy aktorów, czytających linki stron konferencji na wikicfp z pliku wikicfp_conf.txt, na tych stronach wyszukuja
# linki do stron konferencji i wrzucaja to do pliku conf.txt


# komenda do testowania komunikacji pomiędzy aktorami
@command()
def greetme(request, message):
    file_content = 'Hello {}!'.format(message['name'])
    request.actor.logger.info(file_content)
    return file_content


# czyta jeden przekazany link na konferencje na wikicfp i szuka tam linku do tej konferencji, zwraca ten link
def find_conf_link_one(url):
    FORBIDDEN_PREFIXES = ['/', 'tel:', 'mailto:', '.', 'http://www.facebook.com', 'http://twitter.com', 'http://www.linkedin.com', 'https://plus.google.com']
    link_home0 = 0
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser').find('div', class_='contsec')
    #print("linkow na stronie jest:", len(soup.find_all('a', href=True)))
    for i in soup.find_all('a'):
        link = i['href']
        if link.startswith('http') & (all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES)):
            link_home0 = link_home0 + 1
            #print(i['href'])
            if link_home0==1:
                #print("link strony konferencji: ", i['href'])
                return i['href']


# czyta konkretne wiersze z pliku wikicfp_conf.txt, znajduje tam linki do stron konferencji i zapisuje do pliku conf.txt
# znajdowanie linku do strony konferencji jest w funkcji conf_link_one(lk)
@command()
def write_conf_link(request, message):
    myfile = open("wikicfp_conf.txt", "r")
    message_values = list(message.values())  # indeksy pol do zczytywania [[0, 4]]
    request.actor.logger.info("Indeks 1-go wiersza w funkcji readfile: "+ str(message_values[0][0]+1))
    request.actor.logger.info("Indeks ostatniego wiersza w funkcji readfile: " + str(message_values[0][1]))
    #request.actor.logger.info("Message data: " + str(message_values))
    pocz=message_values[0][0]
    koniec=message_values[0][1]
    lines = myfile.readlines()[pocz:koniec]
    #print("wiersz linkow: ", lines)
    #print(lines)
    iter=0
    f = open('conf.txt', 'a')
    while pocz < koniec:
        print("link z wikicfp: ",lines[iter])
        lk = lines[iter].strip()
        #print ("lk=", lk)
        link_conf = find_conf_link_one(lk)
        pocz=pocz+1
        iter = iter + 1
        if link_conf==None:
            print("link strony konferencji: nie ma linka na konferencje")
            continue
        print("link strony konferencji: ", link_conf)
        f.write(link_conf + '\n')
    f.close()
    myfile.close()


class Reader: # czytanie linkow stron konferencji na wikicfp z pliku wikicfp_conf.txt, na tych stronach wyszukiwanie
# linkow do stron konferencji i wrzucanie do pliku conf.txt

    def __init__(self):
        a = arbiter()
        file_length = file_len(FILE_NAME_HOMEPAGES)
        print("File length: " + str(file_length))

        actors_number = len(NAMES) # ilosc aktorow
        print("Number of arbiters: " + str(actors_number))
        self.line_dict = dict.fromkeys(NAMES, [None] * 2)  # słownik, przechowujący listy wskazujące na pierwszą i ostatnią linię, które aktor musi
                                                            # przeczytać z pliku
        indexes = np.arange(0, file_length if file_length % actors_number == 0
                                else file_length - actors_number, file_length // actors_number)  # indexes =  [ 0  5 10 15 20]

        indexes = indexes.tolist()  # zwraca liste indeksow indexes =  [0, 5, 10, 15, 20]
        print("Indeksy bez ostatniego: " + str(indexes))
        indexes.append(file_length) # dadaje na koniec listy element=dlugosci listy, indexes =  [0, 5, 10, 15, 20, 26]

        # TODO: poprawić, żeby ładniej było!
        print("Indeksy: " + str(indexes))
        counter = 0
        for i in self.line_dict: # wpisujemy indeksy do slownika {'reader_2': [0, 4], 'reader_1': [5, 9], 'reader_3': [10, 14], 'reader_5': [15, 19], 'reader_4': [20, 25]}
            #self.line_dict[i] = [indexes[counter], indexes[counter+1]-1]
            self.line_dict[i] = [indexes[counter], indexes[counter + 1]]
            counter += 1

        print(self.line_dict)

        #czyszczenie tekstowego pliku
        f = open('conf.txt', 'w')
        f.close()

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
                print("NAME INDEXES DICT: " + str(name_index_dict))

                # aktor uzywa funkcji write_conf_link do zczytywania z pliku przydzielonych dla niego linkow i zapisywania wynikow do pliku conf.txt:
                # a - aktor, 'write_conf_link' - nazwa wywolywanej funkcji, name_index_dict - parametry przekazywan do funkcji('reader_5', [0, 4])
                await send(a, 'write_conf_link', name_index_dict)

                self._loop.call_later(1, self, a)
        else:
            arbiter().stop()


# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    Reader()









