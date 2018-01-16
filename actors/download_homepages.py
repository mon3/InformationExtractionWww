from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send
from pulsar.api import get_actor
import numpy as np
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer


@command()
async def download_homepages(request, message):

    current_actor = get_actor()
    request.actor.logger.info("Download homepages: " + str(current_actor) + " Urls: " + str(message))

    urls = message
    https = []
    for url in urls:
        with urllib.request.urlopen(url) as conn:
            http = conn.read()
            https.append(http)
            print("Http: ", http)

    return get_actor().name