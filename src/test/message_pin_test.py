'''
TODO: test file for message_pin_test.py
'''

import pytest
import message
import channels
import channel
import error
from data import get_data
import sys
sys.path.append('../')

# Pin successfully
def test_message_pin(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1
    
    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # Pin this message
    message.message_pin(token=token1,message_id=msg_id)
    
    # Check if pinned successfully
    message_object = get_data().get_message_with_message_id(msg_id)
    assert message_object.get_is_pinned()

    get_data().reset()

# Pin an invalid message
def test_message_pin_invalid_message(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1
    
    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # Pin this message
    with pytest.raises(error.InputError):
        message.message_pin(token=token1,message_id=msg_id+1)

    get_data().reset()

# Pinned by a user who is not the owner
def test_message_pin_not_by_owner(get_new_user_1, get_new_user_2):

    # Register test user1 (owner)
    _, token1 = get_new_user_1

    # Register test user1 (common user)
    _, token2 = get_new_user_2
    
    # User1 reate test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']

    # User2 join the channel
    channel.channel_join(token=token2, channel_id=ch_id)

    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # Pin this message
    with pytest.raises(error.InputError):
        message.message_pin(token=token2,message_id=msg_id+1)

    get_data().reset()

# Pin already pinned message
def test_message_react_to_invalid_react_id(get_new_user_1):

    # Register test user1 (owner)
    _, token1 = get_new_user_1

    # User1 reate test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']

    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # Pin this message
    message.message_pin(token=token1,message_id=msg_id)
    with pytest.raises(error.InputError):
        message.message_pin(token=token1,message_id=msg_id)

    get_data().reset()

# Pin by a user who is not a member
def test_message_not_by_a_member(get_new_user_1):

    # Register test user1 (owner)
    _, token1 = get_new_user_1

    # User1 reate test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']

    # Send a message
    msg_send = 'The quick brown fox jumps over the lazy dog'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # Pin this message
    with pytest.raises(error.AccessError):
        message.message_pin(token=token1+'1',message_id=msg_id)

    get_data().reset()