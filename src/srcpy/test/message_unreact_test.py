'''
TODO: test file for message_unreact.py
'''

import pytest
import message
import channels
import error
from data import get_data
import sys
sys.path.append('../')

# Unreact successfully
def test_message_unreact(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1
    
    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # React to this message
    r_id = 1   
    message.message_react(token=token1, message_id=msg_id, react_id=r_id)   

    # Unreact to this message
    message.message_unreact(token=token1, message_id=msg_id, react_id=r_id) 
    
    # Check if unreact successfully
    message_object = get_data().get_message_with_message_id(msg_id)
    react_list = message_object.get_react_list()
    for react in react_list:
        if react.get_react_id() == r_id:
            assert u_id1 not in react.get_u_id_list()
            assert not react.get_is_this_user_reacted()

    get_data().reset()

# Unreact to an invalid message
def test_message_unreact_to_invalid_message(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1
    
    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # React to this message
    r_id = 1
    with pytest.raises(error.InputError):
        message.message_unreact(token=token1, message_id=msg_id+1, react_id=r_id)

    get_data().reset()

# Unreact to an invalid react id
def test_message_unreact_to_invalid_react_id(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1
    
    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # React to this message
    r_id = 2
    with pytest.raises(error.InputError):
        message.message_unreact(token=token1, message_id=msg_id, react_id=r_id)

    get_data().reset()   

# Uneact to a not active react id
def test_message_unreact_not_active(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1
    
    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    assert u_id1 not in get_data().get_message_with_message_id(msg_id).get_react_with_react_id(1).get_u_id_list()
    assert get_data().get_message_with_message_id(msg_id).get_react_with_react_id(1).get_is_this_user_reacted() == False
    # React to this message
    r_id = 1
    message_object = get_data().get_message_with_message_id(msg_id)
    with pytest.raises(error.InputError):
        message.message_unreact(token=token1, message_id=msg_id, react_id=r_id)

    get_data().reset()