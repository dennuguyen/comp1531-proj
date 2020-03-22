'''
util file for message.py
'''

import time
from queue import PriorityQueue

CURRENT_TIME = int(time.time())

def get_current_time():
    global CURRENT_TIME
    return CURRENT_TIME

MESSAGE_QUEUE = PriorityQueue()

def get_message_queue():
    global MESSAGE_QUEUE
    return MESSAGE_QUEUE
