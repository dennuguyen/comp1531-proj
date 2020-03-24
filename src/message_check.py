'''
check the validity of data for functions in message.py
'''
from data import getData
from message_util import get_current_time

def is_valid_message(message):
    return True if len(message) <= 1000 else False

def is_valid_channel(channel_id):
    return True if channel_id in getData().get_all_channel_ids() else False

def is_user_in_channel(u_id, channel_id):
    return True if u_id in getData().get_u_ids_with_channel_id(channel_id) else False

def is_valid_time(time_sent):
    return True if time_sent >= get_current_time() else False

def is_message_in_channel(message_id, channel_id):
    return True if getData().get_channel_id(message_id) == channel_id else False

def is_there_message(message_id):
    return True if getData().get_message(message_id) else False

def is_valid_react_id(react_id):
    return True if react_id == 1 else False

def is_reacted(message_id, react_id):
    return True if getData().get_message(message_id).get_react_dict(react_id)['is_this_user_reacted'] else False

def is_user_the_owner(u_id, channel_id):
    return True if u_id in getData().get_channel_dict(channel_id)['owner_u_ids'] else False

def is_pinned(message_id):
    return True if getData().get_message_dict(message_id)['is_pinned'] else False

def is_message_sent_by_user(message_id, u_id):
    return True if getData().get_message_dict(message_id)['u_id'] == u_id else False