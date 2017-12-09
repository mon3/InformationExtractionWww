# coding=utf-8
import _pickle as cPickle
from pulsar.api import arbiter, spawn, get_actor
from pulsar.apps import Application


#
# import unittest
# import asyncio
#
# from pulsar.api import send, spawn, get_actor, arbiter as get_arbiter


# wysyłanie tasku
# def task(actor, exc=None):
#     # do something useful here
#     ...
#
# ap = spawn(periodic_task=task)


def read_file(actor):
    print("Entering read_file...")
    with open("websites.txt", "r") as f:
        # cl = cPickle.load(f)
        print(f.readline())
    # return cl


class WwwExtraction(Application):

    def build(self):
        print("Application is built")




if __name__ == '__main__':
    print("Main")
    a = arbiter()
    # a.is_running()
    # start arbiter
    a.start()
    # a.is_running()
    # actor1 = get_actor()
    # actor1.start()
    # a.spawn(actor1, periodic_task=read_file)
    a.spawn(start=read_file)

    a.aid
    # a.end()
