import requests
from bs4 import BeautifulSoup, SoupStrainer


url='http://www.wikicfp.com/cfp/allcfp?page=1'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser', parse_only=SoupStrainer('a'))
#print([link['href'] for link in soup if link.has_attr('href')])
ii=0
link_home=0
for link in soup:
    if link.has_attr('href'):
        print("http://www.wikicfp.com" +link['href'])
        link_home=link_home+1
    ii=ii+1
print(ii)
print("link_home = ", link_home)

print("---------test2---------")

import urllib.request
from bs4 import BeautifulSoup

link_home0=0
html = urllib.request.urlopen('http://www.wikicfp.com/cfp/allcfp?page=1')
soup = BeautifulSoup(html, 'html.parser').find('div', class_='contsec')
print("len", len(soup.find_all('a', href=True)))
count=0
for i in soup.find_all('a', href=True):
    count=count+1
    if count<=20:
        print("http://www.wikicfp.com" +i['href'])
        link_home0=link_home0+1
print(link_home0)


print("---------test3 page 2---------")

import urllib.request
from bs4 import BeautifulSoup

link_home0=0
html = urllib.request.urlopen('http://www.wikicfp.com/cfp/allcfp?page=8')
soup = BeautifulSoup(html, 'html.parser').find('div', class_='contsec')
print("len", len(soup.find_all('a', href=True)))
count=0
for i in soup.find_all('a', href=True):
    count=count+1
    if count<=20:
        print("http://www.wikicfp.com" +i['href'])
        link_home0=link_home0+1
print(link_home0)
