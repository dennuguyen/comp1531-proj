import pytest
import message
import auth
import channel
import channels
import error


# User sends a message to a channel they are a member of
def test_message_send_member(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Actual test
    msg_send1 = 'The quick brown fox jumps over the lazy dog'
    msg_id1 = message.message_send(token1, ch_id, msg_send1)['message_id']
    start = 0
    ch_msg_retval = channel.channel_messages(token1, ch_id, start)
    assert ch_msg_retval['messages'][0]['message_id'] == msg_id1
    assert ch_msg_retval['messages'][0]['message'] == msg_send1

    # Confirm next message test
    msg_send2 = 'The quick brown dog jumps over the lazy fox'
    msg_id2 = message.message_send(token1, ch_id, msg_send2)['message_id']
    ch_msg_retval = channel.channel_messages(token1, ch_id, start)
    assert ch_msg_retval['messages'][1]['message_id'] == msg_id2
    assert ch_msg_retval['messages'][1]['message'] == msg_send2


# Stranger to channel sends a message to that channel
def test_message_send_stranger(get_new_user_1, get_new_user_2):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1

    # Register test user 2 (stranger)
    u_id2, token2 = get_new_user_2

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Actual test
    msg_send = 'The quick brown fox jumps over the lazy dog'
    with pytest.raises(error.AccessError):
        message.message_send(token2, ch_id, msg_send)


# Message is more than 1000 char
def test_message_send_1000_char(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Actual test
    msg_send = ('T' * 1001)
    message.message_send(token1, ch_id, msg_send)
    with pytest.raises(error.InputError):
        message.message_send(token1, ch_id, msg_send)
