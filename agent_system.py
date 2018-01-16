from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send
from pulsar.api import get_actor
import numpy as np
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer


def file_len(fname):    # funkcja obliczania dlugosci pliku
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


WIKICFP_FILE = "wikicfp_conf.txt"
FIRST_LEVEL_ACTORS_NUMBER = 5


FIRST_LEVEL_ACTORS = ['get_homepages_1', 'get_homepages_2', 'get_homepages_3', 'get_homepages_4', 'get_homepages_5']
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


@command()
async def delegated(request, message):
    print("Delegated", message)
    return "YYY"
# czyta konkretne wiersze z pliku wikicfp_conf.txt, znajduje tam linki do stron konferencji i zapisuje do pliku conf.txt
# znajdowanie linku do strony konferencji jest w funkcji conf_link_one(lk)
@command()
async def write_conf_link(request, message):
    actor = get_actor()
    print("Actor: ", actor, message)
    test = await spawn(name="xxx")
    res = await send(test, 'delegated', message)
    print("RES", res)
    await send(test, 'stop')
    return

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



class MainArbiter:
    # Klasa uruchamiajaca agentow pierwszego stopnia: czytanie linkow stron konferencji na wikicfp z pliku
    # wikicfp_conf.txt, na tych stronach wyszukiwanie linkow do stron konferencji i wrzucanie do pliku conf.txt

    def __init__(self):
        main_arbiter = arbiter()
        self._loop = main_arbiter._loop    # kod z przykladu w dokumentacji
        self._loop.call_later(1, self)
        self.i = 0
        main_arbiter.start()

    def __call__(self, a=None): # kod z przykladu w dokumentacji
        ensure_future(self._work(a))

    async def _work(self, a=None):
        indexes_pair_dict = self.prepare_indexes()

        #czyszczenie tekstowego pliku
        f = open('conf.txt', 'w')
        f.close()

        spawned_actors = []
        for actor_name in FIRST_LEVEL_ACTORS:
            spawned_actors.append(spawn(name=actor_name))

        for actor in spawned_actors:
            await actor

        sent_actions = []
        for actor in spawned_actors:
            sent_actions.append(send(actor, 'write_conf_link', self.i))
            self.i += 1

        print("Awaiting")

        for action in sent_actions:
            await action

        print("CLOSING")
        for actor in spawned_actors:
            await send(actor, 'stop')

        self._loop.call_later(5, self, a)

    def prepare_indexes(self):
        wikicfp_file_length = file_len(WIKICFP_FILE)
        print("Number of records: " + str(wikicfp_file_length))

        actors_number = len(FIRST_LEVEL_ACTORS)
        print("Number of first level actors: " + str(actors_number))

        line_dict = dict.fromkeys(FIRST_LEVEL_ACTORS, [None] * 2)

        indexes = np.arange(0, wikicfp_file_length if wikicfp_file_length % actors_number == 0
        else wikicfp_file_length - actors_number, wikicfp_file_length // actors_number)  # indexes =  [ 0  5 10 15 20]

        indexes = indexes.tolist()  # zwraca liste indeksow indexes =  [0, 5, 10, 15, 20]
        print("Indeksy bez ostatniego: " + str(indexes))
        indexes.append(wikicfp_file_length)  # dadaje na koniec listy element=dlugosci listy, indexes =  [0, 5, 10, 15, 20, 26]

        counter = 0
        for i in line_dict:  # wpisujemy indeksy do slownika {'reader_2': [0, 4], 'reader_1': [5, 9], 'reader_3': [10, 14], 'reader_5': [15, 19], 'reader_4': [20, 25]}
            # self.line_dict[i] = [indexes[counter], indexes[counter+1]-1]
            line_dict[i] = [indexes[counter], indexes[counter + 1]]
            counter += 1

        return line_dict


# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    MainArbiter()
    original_links()








