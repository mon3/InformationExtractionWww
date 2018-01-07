import urllib.request
import requests
from bs4 import BeautifulSoup, SoupStrainer


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




wikicfp_link(5, 5)
conf_link2()

