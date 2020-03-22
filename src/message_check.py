'''
check the validity of data for functions in message.py
'''
from data import getData

def is_valid_message(message):
    return True

def is_valid_channel(channel_id):
    return True

def is_user_in_channel(u_id, channel_id):
    return True

def is_valid_time(time_sent):
    return True

def is_valid_reaction(reaction):
    return True

def is_message_in_channel(message_id, channel_id):
    return True

def is_there_message(message_id):
    return True

def is_valid_react_id(react_id):
    return True if react_id == 1 else False

def is_not_reacted_yet(message_id, react_id):
    return True