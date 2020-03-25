'''
util file for message.py
'''

import time

CURRENT_TIME = int(time.time())

def get_current_time():
    global CURRENT_TIME
    return CURRENT_TIME