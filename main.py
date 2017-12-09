# coding=utf-8
import pulsar
from pulsar.api import arbiter, spawn
#from pulsar import spawn


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






if __name__ == '__main__':
    print("Main")
    a = arbiter()
    a.is_running()
    # start arbiter
    a.start()