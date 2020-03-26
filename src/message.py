'''
Message related operations are here.
'''

import time
import authenticate as au
from data import get_data, Message

@au.authenticator(au.is_token_valid,
                  au.message_length,
                  au.is_not_member)
def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified
    by channel_id
    '''
    u_id = get_data().get_user_with_token(token).get_u_id()

    # setup the message
    message_id = get_data().global_msg_id()
    time_created = int(time.time())
    message_object = Message(message_id, u_id, message, time_created)

    # update the database
    get_data().add_message(message_object)
    channel = get_data().get_channel_with_ch_id(channel_id)
    channel.add_new_message(message_id)

    return {
        'message_id': message_id
    }

@au.authenticator(au.is_token_valid,
                  au.valid_channel_id,
                  au.message_length,
                  au.send_message_in_future,
                  au.is_not_member)
def message_sendlater(token, channel_id, message, time_sent):
    '''
    Send a message from authorised_user to the channel specified
    by channel_id automatically at a specified time in the future
    '''
    u_id = get_data().get_user_with_token(token).get_u_id()

    # setup the message
    message_id = get_data().global_msg_id()
    time_created = int(time.time())
    message_object = Message(message_id, u_id, message, time_created)

    # update the database
    get_data().add_message_later(message_object)

    return {
        'message_id': message_id
    }

@au.authenticator(au.is_token_valid,
                  au.is_message_id_in_channel,
                  au.is_valid_react_id,
                  au.already_contains_react)
def message_react(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of,
    add a "react" to that particular message
    '''

    # update the database
    u_id = get_data().get_user_with_token(token).get_u_id()
    message_object = get_data().get_message_with_message_id(message_id)
    message_object.set_react(react_id, u_id, True)

    return {}

@au.authenticator(au.is_token_valid,
                  au.is_message_id_in_channel,
                  au.is_valid_react_id,
                  au.does_not_contain_react)
def message_unreact(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of,
    remove a "react" to that particular message
    '''

    # update the database
    u_id = get_data().get_user_with_token(token).get_u_id()
    message_object = get_data().get_message_with_message_id(message_id)
    message_object.set_react(react_id, u_id, False)

    return {}

@au.authenticator(au.is_token_valid,
                  au.message_id_valid,
                  au.is_private_not_admin,
                  au.message_already_pinned,
                  au.user_not_member_using_message_id)
def message_pin(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to be given
    special display treatment by the frontend
    '''

    # update the database
    message_object = get_data().get_message_with_message_id(message_id)
    message_object.set_is_pinned(True)

    return {}

@au.authenticator(au.is_token_valid,
                  au.message_id_valid,
                  au.is_private_not_admin,
                  au.message_already_unpinned,
                  au.user_not_member_using_message_id)
def message_unpin(token, message_id):
    '''
    Given a message within a channel, remove it's mark as unpinned
    '''

    # update the database
    message_object = get_data().get_message_with_message_id(message_id)
    message_object.set_is_pinned(False)

    return {}

@au.authenticator(au.is_token_valid,
                  au.message_id_valid,
                  au.edit_permissions)
def message_remove(token, message_id):
    '''
    Given a message_id for a message,
    this message is removed from the channel
    '''

    # update the database
    message_object = get_data().get_message_with_message_id(message_id)
    get_data().remove_message(message_object)
    for channel in get_data().get_channel_list():
        for msg_id in channel.get_msg_id_list():
            if msg_id == message_id:
                channel.remove_message(message_id)

    return {}

@au.authenticator(au.is_token_valid,
                  au.edit_permissions)
def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text.
    If the new message is an empty string, the message is deleted.
    '''
    #  If the message is an empty string, delete it.
    if not message:
        message_remove(token, message_id)

    # update the database
    message_object = get_data().get_message_with_message_id(message_id)
    message_object.set_message(message)

    return {}
