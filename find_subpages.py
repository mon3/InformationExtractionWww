import urllib.request
from bs4 import BeautifulSoup


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


wikicfp_link(2)
