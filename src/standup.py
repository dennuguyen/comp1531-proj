'''
Standup related functions are here
'''

import time
import message
import data
import authenticate as au

@au.authenticator(au.is_token_valid, au.valid_channel_id, au.already_active_standup)
def standup_start(* ,token, channel_id, length):
    ''' Add a message to the message queue at the end of the message queue in channel.'''

     # start a standup
    data.get_data().get_channel_with_ch_id(channel_id).set_clear_standup_queue() 
    channel = data.get_data().get_channel_with_ch_id(channel_id)
    channel.set_standup_status(True)
    channel.set_standup_time_finish(int(time.time())+length)
    time_finish = channel.get_standup_time_finish()
    time.sleep(length)
    standup_delivery(token=token, channel_id=channel_id)
    data.get_data().get_channel_with_ch_id(channel_id).set_clear_standup_queue()
    return {'time_finish' : time_finish}


@au.authenticator(au.is_token_valid, au.valid_channel_id)
def standup_active(*, token, channel_id):
    ''' For a given channel, return whether a standup is active in it, and what time the standup finishes. '''

    channel = data.get_data().get_channel_with_ch_id(channel_id)
    return {
        'is_active' : channel.get_is_active_standup(),
        'time_finish' : channel.get_standup_time_finish()
    }

@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_token_in_channel, au.message_length)
def standup_send(*, token, channel_id, message):
    ''' Sending a message to get buffered in the standup queue, assuming a standup is currently active.'''

    # setup
    user = data.get_data().get_user_with_token(token)
    users_name = user.get_name_first()
    channel = data.get_data().get_channel_with_ch_id(channel_id)

    # update the database
    New_standup = {'name' : users_name, 'message' : message}
    channel.add_message_to_standup_queue(New_standup)
    return {}

def standup_packaging(*, channel_id):
    standup_queue = data.get_data().get_channel_with_ch_id(channel_id).get_standup_queue()
    standup_package = ''
    for standup_data in standup_queue:
        standup_package += standup_data['name'] + ': ' + standup_data['message'] + '\n'
    return standup_package

def standup_delivery(*, token, channel_id):
    standup_package = standup_packaging(channel_id=channel_id)
    message.message_send(token=token, channel_id=channel_id, message=standup_package)
    channel = data.get_data().get_channel_with_ch_id(channel_id)
    channel.set_standup_status(False)
    channel.set_standup_time_finish(None)
    return