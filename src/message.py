'''
Message related operations are here.
'''

import message_check
import message_data
import error


def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified 
    by channel_id
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
    '''
    Given a message within a channel the authorised user is part of, 
    add a "react" to that particular message
    '''
    u_id = message_data.get_uid_with_token(token)
    if not message_check.is_user_in_channel(u_id, channel_id):
        raise error.AccessError(description = "The user is not in this channel")
    if not message_check.is_message_in_channel(message_id, channel_id):
        raise error.AccessError(description = "The message is not in this channel")
    

    return {}

def message_unreact(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of,
    remove a "react" to that particular message
    '''
    return {}

def message_pin(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to be given 
    special display treatment by the frontend
    '''
    return {}

def message_unpin(token, message_id):
    '''
    Given a message within a channel, remove it's mark as unpinned
    '''
    return {}

def message_remove(token, message_id):
    '''
    Given a message_id for a message, 
    this message is removed from the channel
    '''
    return {}

def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text. 
    If the new message is an empty string, the message is deleted.
    '''
    return {}
