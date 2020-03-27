'''
TODO: test file for message_react.py
'''

import pytest
import message
import channels
import error
from data import get_data
import sys
sys.path.append('../')

# React successfully
def test_message_react(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1
    
    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # React to this message
    print('[here_1]')
    print(get_data().get_message_with_message_id(msg_id).get_react_with_react_id(1).get_u_id_list())
    print(get_data().get_message_with_message_id(msg_id).get_react_with_react_id(1).get_is_this_user_reacted())
    r_id = 1
    
    message.message_react(token=token1, message_id=msg_id, react_id=r_id)
    

    # Check if react successfully
    message_object = get_data().get_message_with_message_id(msg_id)
    react_list = message_object.get_react_list()
    for react in react_list:
        if react.get_react_id() == r_id:
            assert u_id1 in react.get_u_id_list()
            assert react.get_is_this_user_reacted() == True

    get_data().reset()

# React to an invalid message
def test_message_react_to_invalid_message(get_new_user_1):


    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1
    
    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # React to this message
    print('[here_2]')
    print(get_data().get_message_with_message_id(msg_id).get_react_with_react_id(1).get_u_id_list())
    print(get_data().get_message_with_message_id(msg_id).get_react_with_react_id(1).get_is_this_user_reacted())
    r_id = 1
    with pytest.raises(error.InputError):
        message.message_react(token=token1, message_id=msg_id+1, react_id=r_id)

    get_data().reset()

# React to an invalid react id
def test_message_react_to_invalid_react_id(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1
    
    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # React to this message
    print('[here_3]')
    print(get_data().get_message_with_message_id(msg_id).get_react_with_react_id(1).get_u_id_list())
    print(get_data().get_message_with_message_id(msg_id).get_react_with_react_id(1).get_is_this_user_reacted())
    r_id = 2
    with pytest.raises(error.InputError):
        message.message_react(token=token1, message_id=msg_id, react_id=r_id)

    get_data().reset()   

# React to an already active react id
def test_message_react_already_active(get_new_user_1):

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
    print('here')
    print(message_object.get_react_with_react_id(r_id).get_u_id_list())
    message.message_react(token=token1, message_id=msg_id, react_id=r_id)
    with pytest.raises(error.InputError):
        message.message_react(token=token1, message_id=msg_id, react_id=r_id)

    get_data().reset()
