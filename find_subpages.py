import urllib.request
import requests
from bs4 import BeautifulSoup, SoupStrainer
from itertools import islice

# wyszukiwanie i pobieranie linkow ze strony http://www.wikicfp.com/cfp/allcfp?page= na podstrony wikicfp do poszczegolnych
# konferencji i zapisywanie ich do pliku wikicfp_conf_orig.txt
def wikicfp_link(number, n2):
    link='http://www.wikicfp.com/cfp/allcfp?page='
    ind=1
    f = open('wikicfp_conf_orig.txt', 'w')
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

