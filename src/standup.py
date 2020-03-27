'''
Standup related functions are here
'''
import time
import threading
from data import get_data, Message
import authenticate as au

@au.authenticator(au.is_token_valid, au.valid_channel_id, au.already_active_standup)
def standup_start(token, channel_id, length):
    ''' Add a message to the message queue at the end of the message queue in channel.'''

     # start a standup
    channel = get_data().get_channel_with_ch_id(channel_id)
    channel.set_standup_status(True)
    channel.set_standup_time_finish(int(time.time())+length)
    threading.Timer(length, channel.pop_standup_queue_into_message_queue())
    
    # reset the data after finishing the standup
    channel.set_standup_status(False)
    channel.set_standup_time_finish(-1)

    return {
        'time_finish' : channel.get_standup_time_finish()
    }

@au.authenticator(au.is_token_valid, au.valid_channel_id)
def standup_active(token, channel_id):
    ''' For a given channel, return whether a standup is active in it, and what time the standup finishes. '''

    channel = get_data().get_channel_with_ch_id(channel_id)
    return {
        'is_active' : channel.get_is_active_standup,
        'time_finish' : channel.get_standup_time_finish()
    }

@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_user_in_channel, au.message_length, au.already_active_standup)
def standup_send(token, channel_id, message):
    ''' Sending a message to get buffered in the standup queue, assuming a standup is currently active.'''

    # setup the message
    u_id = get_data().get_user_with_token(token).get_u_id()
    message_id = get_data().global_msg_id()
    time_created = int(time.time())
    message_object = Message(message_id, u_id, message, time_created)

     # update the database
    get_data().add_message(message_object)
    channel = get_data().get_channel_with_ch_id(channel_id)
    channel.add_message_to_standup_queue(message_id)

    return {}
