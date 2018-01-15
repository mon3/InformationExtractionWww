from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send
import numpy as np
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer


def file_len(fname):    # funkcja obliczania dlugosci pliku
    with open(fname) as f:
        for i, l in enumerate(f):
            #print("i=", i)
            pass
    return i + 1


FILE_NAME_HOMEPAGES = "wikicfp_conf.txt"

NAMES = ['reader_1', 'reader_2', 'reader_3', 'reader_4', 'reader_5']
# nazwy aktorów, czytających linki stron konferencji na wikicfp z pliku wikicfp_conf.txt, na tych stronach wyszukuja
# linki do stron konferencji i wrzucaja to do pliku conf.txt


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
    message_values = list(message.values())
    request.actor.logger.info("Indeks 1-go wiersza w funkcji readfile: "+ str(message_values[0][0]+1))
    request.actor.logger.info("Indeks ostatniego wiersza w funkcji readfile: " + str(message_values[0][1]))
    #request.actor.logger.info("Message data: " + str(message_values))
    pocz=message_values[0][0]
    koniec=message_values[0][1]
    lines = myfile.readlines()[pocz:koniec]
    # print("wiersz linkow: ", lines)
    #print(lines)
    iter=0
    f = open('conf.txt', 'a')
    while pocz < koniec:
        #print("link z wikicfp: ",lines[iter])
        lk = lines[iter].strip()
        #print ("lk=", lk)
        link_conf = find_conf_link_one(lk)
        pocz=pocz+1
        iter = iter + 1
        if link_conf==None:
            #print("link strony konferencji: nie ma linka na konferencje")
            continue
        #print("link strony konferencji: ", link_conf)
        f.write(link_conf + '\n')
    f.close()
    myfile.close()

def original_links():
    file = open('conf.txt', 'r')
    lines = file.readlines()
    file.close()
    file = open('conf.txt', 'w')
    List = list(set(lines))
    iter=0
    while iter<len(List):
        file.write(List[iter])
        iter = iter + 1
    file.close()



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
            name = NAMES.pop()
            # słownik nie może być pusty - inaczej rzuca błędem
            if (len(self.line_dict)!=0):
                name_indexes = self.line_dict.popitem()
                print("NAME INDEXES: " + str(name_indexes))

                name_index_dict = {name_indexes[0]: name_indexes[1]}
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
    original_links()








