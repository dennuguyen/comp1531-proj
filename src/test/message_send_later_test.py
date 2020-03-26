'''
TODO: test file for message_send_later_test.py
'''

import pytest
import message
import channel
import channels
import error
import time
import other
from data import get_data
import sys
sys.path.append('../')

# User sends a message to a channel they are a member of
def test_message_sendlater_member(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1
    
    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    # Send message 1
    msg_send1 = 'The quick brown fox jumps over the lazy dog'
    time_to_be_sent = int(time.time()) + 60
    msg_id1 = message.message_sendlater(token=token1, channel_id=ch_id, message=msg_send1, time_sent=time_to_be_sent)['message_id']

    # Check message 1
    message_object1 = get_data().get_message_wl_with_message_id(msg_id1)

    assert message_object1 in get_data().get_message_wait_list()

    # Send message 2
    msg_send2 = 'The quick brown dog jumps over the lazy fox'
    time_to_be_sent = int(time.time()) + 90
    msg_id2 = message.message_sendlater(token=token1, channel_id=ch_id, message=msg_send2, time_sent=time_to_be_sent)['message_id']

    # Check message 2
    message_object2 = get_data().get_message_wl_with_message_id(msg_id2)
    assert message_object2 in get_data().get_message_wait_list()

    # Check both messages are in channel
    assert len(get_data().get_message_wait_list()) == 2

    get_data().reset()


# Stranger to channel sends a message to that channel
def test_message_sendlater_stranger(get_new_user_1, get_new_user_2):

    # Register test user 1 (owner)
    print(get_data().get_user_with_email('hugh_jackman@unsw.com'))
    _, token1 = get_new_user_1

    # Register test user 2 (stranger)
    _, token2 = get_new_user_2

    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']

    # Actual test
    msg_send = 'The quick brown fox jumps over the lazy dog'
    time_to_be_sent = int(time.time()) + 60
    with pytest.raises(error.AccessError):
        message.message_sendlater(token=token2, channel_id=ch_id, message=msg_send, time_sent=time_to_be_sent)

    get_data().reset()


# Message is more than 1000 char
def test_message_sendlater_1000_char(get_new_user_1):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']

    # Actual test
    msg_send = ('T' * 1001)
    time_to_be_sent = int(time.time()) + 60
    with pytest.raises(error.InputError):
        message.message_sendlater(token=token1, channel_id=ch_id, message=msg_send, time_sent=time_to_be_sent)

    get_data().reset()

# Message sent time is set before current time
def test_message_sendlater_in_the_future(get_new_user_1):
    
    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']

    # Actual test
    msg_send = 'The quick brown fox jumps over the lazy dog'
    time_to_be_sent = int(time.time()) - 60
    with pytest.raises(error.InputError):
        message.message_sendlater(token=token1, channel_id=ch_id, message=msg_send, time_sent=time_to_be_sent)

    get_data().reset()

# Channel id is not valid
def test_message_sendlater_in_valid_channel(get_new_user_1):
    
    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']

    # Actual test
    msg_send = 'The quick brown fox jumps over the lazy dog'
    time_to_be_sent = int(time.time())
    with pytest.raises(error.InputError):
        message.message_sendlater(token=token1, channel_id=ch_id+1, message=msg_send, time_sent=time_to_be_sent)

    get_data().reset()