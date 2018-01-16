import numpy as np
import urllib.request
from asyncio import ensure_future
from bs4 import BeautifulSoup, SoupStrainer
from pulsar.api import arbiter, command, spawn, send
from pulsar.api import get_actor

from actors import download_homepages

CONFERENCES_HOMEPAGES_FILENAME ='working_files/conferences_homepages.txt'
WIKICFP_FILENAME = 'working_files/wikicfp_conf.txt'


def split_to_chunks(list, splits_number):
    avg = len(list) / float(splits_number)
    out = []
    last = 0.0
    while last < len(list):
        out.append(list[int(last):int(last + avg)])
        last += avg
    return out

# czyta jeden przekazany link na konferencje na wikicfp i szuka tam linku do tej konferencji, zwraca ten link
def find_conf_link_one(url):
    FORBIDDEN_PREFIXES = ['/', 'tel:', 'mailto:', '.', 'http://www.facebook.com', 'http://twitter.com',
                          'http://www.linkedin.com', 'https://plus.google.com']
    link_home0 = 0
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser').find('div', class_='contsec')
    # print("linkow na stronie jest:", len(soup.find_all('a', href=True)))
    for i in soup.find_all('a'):
        link = i['href']
        if link.startswith('http') & (all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES)):
            link_home0 = link_home0 + 1
            if link_home0 == 1:
                # print("link strony konferencji: ", i['href'])
                return i['href']

"""
Actor used for getting homepages links from wikicpf entries stored in wikicfp_conf_orig.txt file.
Next, it creates new actors who download pages and split them between extractor actors.
"""
@command()
async def parse_homepages_from_wiki_lvl1(request, message):

    current_actor = get_actor()
    request.actor.logger.info("Actor: " + str(current_actor) + " Indexes: " +  str(message))

    wikicfp_file = open(WIKICFP_FILENAME, "r")
    wikicfp_file_lines = wikicfp_file.readlines()[message[0]: message[1]]
    wikicfp_file.close()

    conference_links = []
    for i in range(len(wikicfp_file_lines)):
        stripped_line = wikicfp_file_lines[i].strip()
        print("Stripped line:" , stripped_line)
        conference_link = find_conf_link_one(stripped_line)
        print("conferecne link", conference_link)
        if conference_link == None:
            continue
        conference_links.append(conference_link)

    f = open(CONFERENCES_HOMEPAGES_FILENAME, 'a')
    for link in conference_links:
        f.write(link + '\n')
    f.close()

    print(conference_links)
    conference_links_chunks = split_to_chunks(conference_links, 4)

    spawned_actors = []
    for i, links_chunk in enumerate(conference_links_chunks):
        spawned_actors.append(spawn(name=current_actor.name+"_"+str(i)))

    for actor in spawned_actors:
        await actor

    sent_actions = []
    for actor, chunk in zip(spawned_actors, conference_links_chunks):
        sent_actions.append(send(actor, 'download_homepages', chunk))

    for action in sent_actions:
        result = await action
        print(result)

    for actor in spawned_actors:
        await send(actor, 'stop')

    return

