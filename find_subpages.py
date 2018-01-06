import urllib.request
import requests
from bs4 import BeautifulSoup, SoupStrainer


def wikicfp_link(number):
    #link_home0=0
    #link='http://www.wikicfp.com/cfp/allcfp?page=2'
    link='http://www.wikicfp.com/cfp/allcfp?page='
    #number = 3 #indeks strony na wikicfp (ile stron musimu przeszukac)
    ind=1

    f = open('wikicfp_conf.txt', 'w')

    while ind <= number:
        html = urllib.request.urlopen(link + str(ind))
        soup = BeautifulSoup(html, 'html.parser').find('div', class_='contsec')
        #print("len", len(soup.find_all('a', href=True)))
        count=0
        #f = open('wikicfp_conf.txt', 'w')
        for i in soup.find_all('a', href=True):
            count=count+1
            if count<=20: # na kazdej stronie jest 20 linkow na konferencje
                f.write("http://www.wikicfp.com" +i['href'] + '\n')
                print("http://www.wikicfp.com" +i['href'])
                #link_home0=link_home0+1
        ind=ind+1
    f.close()
    #print(link_home0)





#wikicfp_link(1)



def conf_link():
    myfile = open("wikicfp_conf.txt", "r")  # чтение из файла
    for line in myfile.readlines():  # построчно читаем файл и выводим на экран
        # print (line)
        url = line.strip()
        #url='http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=71733&copyownerid=13881'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser', parse_only=SoupStrainer('a'))
        #soup = BeautifulSoup(r.content, 'html.parser').find('td', align_='center')
        #print([link['href'] for link in soup if link.has_attr('href')])
        print("linkow na stronie jest:", len(soup.find_all('a', href=True)))
        ii=0
        link_home=0
        for link in soup:
            ii = ii + 1
            if ii==25 :
                print("link strony konferencji: ", link['href'])
                link_home=link_home+1

        #print(ii)
        print("link_home = ", link_home)


#conf_link()


# td align="center"

def ww():
    print("---------test3 page 2---------")

    import urllib.request
    from bs4 import BeautifulSoup

    link_home0=0
    html = urllib.request.urlopen('http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=71777&copyownerid=89732')
    soup = BeautifulSoup(html, 'html.parser').find('div', class_='contsec')
    print("len", len(soup.find_all('a', href=True)))
    count=0
    for i in soup.find_all('a', href=True):
        #if not i.startswith('/') and not i.startswith('tel:'):
        count=count+1
        #if count<=20:
        print(i['href'])
        link_home0=link_home0+1
    print(link_home0)


from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
#import lxml

FORBIDDEN_PREFIXES = ['/', 'tel:', 'mailto:', '.']

url='http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=71777&copyownerid=89732'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser', parse_only=SoupStrainer('a'))
link_home0 = 0
for i in soup.find_all('a'):
    link = i['href']
    #if not link.startswith('/'):
    if all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
    #if not link.startswith()
        print(i['href'])
        link_home0 = link_home0 + 1
print(link_home0)


