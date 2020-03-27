'''
Standup related functions are here
'''
import time
import message
import threading
import data
import authenticate as au

@au.authenticator(au.is_token_valid, au.valid_channel_id, au.already_active_standup)
def standup_start(* ,token, channel_id, length):
    ''' Add a message to the message queue at the end of the message queue in channel.'''

     # start a standup
    channel = data.get_data().get_channel_with_ch_id(channel_id)
    channel.set_standup_status(True)
    channel.set_standup_time_finish(int(time.time())+length)
    standup_package = standup_packaging(channel_id=channel_id)
    message.message_send(token=token, channel_id=channel_id, message=standup_package)
    threading.Timer(length, channel.pop_standup_queue_into_message_queue())
    
    # reset the data after finishing the standup
    channel.set_standup_status(False)
    channel.set_standup_time_finish(None)

    return {
        'time_finish' : channel.get_standup_time_finish()
    }

@au.authenticator(au.is_token_valid, au.valid_channel_id)
def standup_active(*, token, channel_id):
    ''' For a given channel, return whether a standup is active in it, and what time the standup finishes. '''

    channel = data.get_data().get_channel_with_ch_id(channel_id)
    return {
        'is_active' : channel.get_is_active_standup(0),
        'time_finish' : channel.get_standup_time_finish()
    }

@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_user_in_channel, au.message_length, au.already_active_standup)
def standup_send(*, token, channel_id, message):
    ''' Sending a message to get buffered in the standup queue, assuming a standup is currently active.'''

    # setup
    user = data.get_data().get_user_with_token(token)
    users_name = user.get_name_first()
    channel = data.get_data().get_channel_with_ch_id(channel_id)

    # update the database
    New_standup = data.Standup(users_name, message)
    channel.add_message_to_standup_queue(New_standup)

    return {}

def standup_packaging(*, channel_id=channel_id):
    standup_queue = data.get_data().get_channel_with_ch_id(channel_id).get_standup_queue()
    standup_package = ''
    for standup_msg in standup_queue:
        standup_package += standup_msg.get_standup_name() + ': ' + standup_msg.get_standup_message() + '\n'
    return standup_package