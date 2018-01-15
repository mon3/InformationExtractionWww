import urllib.request
import requests
from bs4 import BeautifulSoup, SoupStrainer
from itertools import islice

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

    #myfile = open("wikicfp_conf.txt", "r")
    #lines = myfile.readlines()
    #print("wikicfp_conf lista z pliku", myfile)
    #myfile.close()

#wikicfp_link(3, 1)



# wyszukiwanie na podstronach wikicfp linkow na strony konferencji typu http://www.icisce.org
# i zapisywanie ich do pliku conf.txt
def conf_link2():
    myfile = open("wikicfp_conf.txt", "r")
    FORBIDDEN_PREFIXES = ['/', 'tel:', 'mailto:', '.', 'http://www.facebook.com', 'http://twitter.com', 'http://www.linkedin.com', 'https://plus.google.com']
    f = open('conf.txt', 'w')
    for line in myfile.readlines():
        # print (line)
        link_home0 = 0
        url = line.strip()
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser').find('div', class_='contsec')
        #print("---------")
        #print("linkow na stronie jest:", len(soup.find_all('a', href=True)))
        for i in soup.find_all('a'):
            link = i['href']
            if link.startswith('http') & (all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES)):
                link_home0 = link_home0 + 1
                #print(i['href'])
                if link_home0==1:
                    f.write(i['href'] + '\n')
                    print("link strony konferencji: ", i['href'])
        #print("link_home0", link_home0)
    f.close()
    myfile.close()

#wikicfp_link(5, 1)
#conf_link2()




# czytanie konkretnych wierszy w pliku
def line():
    file = open('wikicfp_conf.txt', 'r')
    #print(islice(file, 5, None))
    #lines = islice(file, 5, None)

    #with open("wikicfp_conf.txt") as file:
    #    lines = file.readlines()
    #lines = ''.join(lines[5:8])
    #print(lines)

    pocz=5
    konec=8
    ra=konec-pocz
    lines = file.readlines()
    print(lines)
    iter=0
    #print(lines[iter])
    while iter<ra:
        print(lines[iter])
        iter = iter + 1
    file.close()


#line()

def original_links():
    file = open('conf.txt', 'r')
    lines = file.readlines()
    file.close()
    file = open('conf.txt', 'w')
    #print("dlina spiska:", len(lines))
    List = list(set(lines))
    #print("lines", lines)
    #print("List", List)
    #print(List[0])
    #print("dlina spiska bez powtorow:", len(List))
    iter=0
    while iter<len(List):
        #print(lines[iter])
        file.write(List[iter])
        iter = iter + 1
    file.close()

#wikicfp_link(2, 2)
#conf_link2()
#original_links()

# czyta jeden przekazany link do konferencji na wikicfp i szuka tam linku do tej konferencji, zwraca ten link
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


#lk='http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=71536&copyownerid=44202'
#a=find_conf_link_one(lk)
#print("a=", a)





# czyta wszystkie wiersze z pliku wikicfp_conf.txt, znajduje tam linki do stron konferencji i zapisuje do pliku conf.txt
# znajdowanie linku do strony konferencji jest w funkcji conf_link_one(lk)
def conf_linkN():
    myfile = open("wikicfp_conf.txt", "r")
    f = open('conf.txt', 'w')
    for line in myfile.readlines():
        lk = line.strip()
        #f.write(i['href'] + '\n')
        link_conf=find_conf_link_one(lk)
        if link_conf==None:
            continue
        print("link strony konferencji: ", link_conf)
        f.write(link_conf + '\n')
    f.close()
    myfile.close()


#conf_linkN()

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

# czyta konkretne wiersze z pliku wikicfp_conf.txt, znajduje tam linki do stron konferencji i zapisuje do pliku conf.txt
# znajdowanie linku do strony konferencji jest w funkcji conf_link_one(lk)
def write_conf_link(pocz, konec):
    myfile = open("wikicfp_conf.txt", "r")
    pocz=pocz-1
    lines = myfile.readlines()[pocz:konec]
    #print(lines)
    iter=0
    #print(lines[iter])
    f = open('conf.txt', 'w')
    while pocz < konec:
        print("link z wikicfp: ",lines[iter])
        lk = lines[iter].strip()
        #print ("lk=", lk)
        link_conf = find_conf_link_one(lk)
        pocz=pocz+1
        iter = iter + 1
        if link_conf==None:
            print("link strony konferencji: nie ma linku na konferencje")
            continue
        print("link strony konferencji: ", link_conf)
        f.write(link_conf + '\n')


    f.close()
    myfile.close()



#write_conf_link(1, 10)



def file_len(fname):    # funkcja obliczania dlugosci pliku
    with open(fname) as f:
        for i, l in enumerate(f):
            #print("i=", i)
            pass
    return i + 1

#print("Dlugosc pliku conf.txt:", file_len('conf.txt'))

