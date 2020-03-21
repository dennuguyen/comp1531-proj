'''
Message related operations are here.
'''

import message_check
import message_data
import error


def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id
    '''
    u_id = message_data.get_uid_with_token(token)

    if not message_check.is_user_in_channel(u_id, channel_id):
        raise error.AccessError(description = "The user is not in this channel")
    if not message_check.is_valid_channel(channel_id):
        raise error.InputError(description = "The channel does not exist")
    if not message_check.is_valid_message(message):
        raise error.InputError(description = "The message is more than 1000 characters")
    
    message_id = message_data.create_message_object(u_id, message)['message_id']
    message_data.add_message_to_channel(u_id, message_id)

    return {
        'message_id': message_id
    }

def message_sendlater(token, channel_id, message, time_sent):
    '''
    Send a message from authorised_user to the channel specified 
    by channel_id automatically at a specified time in the future
    '''
    u_id = message_data.get_uid_with_token(token)

    if not message_check.is_user_in_channel(u_id, channel_id):
        raise error.AccessError(description = "The user is not in this channel")
    if not message_check.is_valid_channel(channel_id):
        raise error.InputError(description = "The channel does not exist")
    if not message_check.is_valid_message(message):
        raise error.InputError(description = "The message is more than 1000 characters")
    if not message_check.is_valid_time(time_sent):
        raise error.InputError(description = "Time sent is a time in the past.")


    message_id = message_data.create_message_object(u_id, message)['message_id']
    message_data.add_message_to_queue(u_id, message_id, time_sent)

    return {
        'message_id': message_id
    }

def message_react(token, message_id, react_id):
    
    return {}

def message_unreact(token, message_id, react_id):
    return {}

def message_pin(token, message_id):
    return {}

def message_unpin(token, message_id):
    return {}

def message_remove(token, message_id):
    return {}

def message_edit(token, message_id, message):
    return {}
