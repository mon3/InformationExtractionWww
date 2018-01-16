from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send
from pulsar.api import get_actor
import numpy as np
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
from actors import download_homepages, extract


@command()
async def download_homepages(request, message):

    print("DOWNLOAD", message)
    current_actor = get_actor()
    request.actor.logger.info("Download homepages: " + str(current_actor) + " Urls: " + str(message))

    urls = message
    https = []
    for url in urls:
        with urllib.request.urlopen(url) as conn:
            http = conn.read()
            https.append([http])


    spawned_actors = []
    for i, http in enumerate(https):
        spawned_actors.append(spawn(name=current_actor.name + "_extractor_" + str(i)))

    for actor in spawned_actors:
        await actor

    sent_actions = []
    for actor, http in zip(spawned_actors, https):
        sent_actions.append(send(actor, 'extract_data', http))

    for action in sent_actions:
        result = await action

    for actor in spawned_actors:
        await send(actor, 'stop')

    return get_actor().name