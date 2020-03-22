'''
Message related operations are here.
'''

import message_check
from data import getData, Message
from message_util import get_current_time
import error
 

def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified 
    by channel_id
    '''
    u_id = getData().get_u_id_with_token(token)
    
    # check validity of the input augments
    if not message_check.is_user_in_channel(u_id, channel_id):
        raise error.AccessError(description="The user is not in this channel.")
    if not message_check.is_valid_channel(channel_id):
        raise error.InputError(description="The channel does not exist.")
    if not message_check.is_valid_message(message):
        raise error.InputError(description="The message is more than 1000 characters.")
    
    # setup the message
    message_id = getData().gen_next_channel_id()
    time_created = get_current_time()
    message_object = Message(message_id, u_id, message, time_created)

    # update the database
    getData().add_message(message_object)
    getData().add_message_to_channel(message_id, channel_id)

    return {
        'message_id': message_id
    }

def message_sendlater(token, channel_id, message, time_sent):
    '''
    Send a message from authorised_user to the channel specified
    by channel_id automatically at a specified time in the future
    '''
    u_id = getData().get_u_id_with_token(token)

    # check validity of the input augments
    if not message_check.is_user_in_channel(u_id, channel_id):
        raise error.AccessError(description="The user is not in this channel.")
    if not message_check.is_valid_channel(channel_id):
        raise error.InputError(description="The channel does not exist.")
    if not message_check.is_valid_message(message):
        raise error.InputError(description="The message is more than 1000 characters.")
    if not message_check.is_valid_time(time_sent):
        raise error.InputError(description="Time sent is a time in the past.")

    # setup the message
    message_id = getData().gen_next_channel_id()
    time_created = get_current_time()
    message_object = Message(message_id, u_id, message, time_created)

    # update the database
    getData().add_message(message_object)
    # !!!!!!!!!!!!!!!!!!!! not solved yet !!!!!!!!!!!!!!!!!!!!!

    return {
        'message_id': message_id
    }

def message_react(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of, 
    add a "react" to that particular message
    '''
    # check validity of the input augments
    if not message_check.is_there_message(message_id):
        raise error.InputError(description="The message does not exsit.")

    u_id = getData().get_u_id_with_token(token)
    channel_id = getData().get_channel_id(message_id)
    if not message_check.is_user_in_channel(u_id, channel_id):
        raise error.InputError(description="The user is not in this channel.")
    if not message_check.is_message_in_channel(message_id, channel_id):
        raise error.InputError(description="The message is not in this channel.")
    
    if not message_check.is_valid_react_id(react_id):
        raise error.InputError(description="This is an invalid reaction.")
    if not message_check.is_not_reacted_yet(message_id, react_id):
        raise error.InputError(description="The message has already been reacted with this reaction.")
    
    # update the database
    message_object = getData().get_message(message_id)
    message_object.set_react(react_id, u_id, True)
    
    return {}

def message_unreact(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of,
    remove a "react" to that particular message
    '''
    # check validity of the input augments
    if not message_check.is_there_message(message_id):
        raise error.InputError(description="The message does not exsit.")

    u_id = getData().get_u_id_with_token(token)
    channel_id = getData().get_channel_id(message_id)
    if not message_check.is_user_in_channel(u_id, channel_id):
        raise error.InputError(description="The user is not in this channel.")
    if not message_check.is_message_in_channel(message_id, channel_id):
        raise error.InputError(description="The message is not in this channel.")
    
    if not message_check.is_valid_react_id(react_id):
        raise error.InputError(description="This is an invalid reaction.")
    if message_check.is_not_reacted_yet(message_id, react_id):
        raise error.InputError(description="The message has not been reacted with this reaction yet.")
    
    # update the database
    message_object = getData().get_message(message_id)
    message_object.set_react(react_id, u_id, False)
    
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
