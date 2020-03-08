import pytest
import message
import auth
import channel
import channels
import error
import datetime
import other


# User sends a message to a channel they are a member of
def test_message_send_member(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Send message 1
    msg_send1 = 'The quick brown fox jumps over the lazy dog'
    time_before1 = datetime.datetime.now()
    msg_id1 = message.message_send(token1, ch_id, msg_send1)['message_id']
    time_after1 = datetime.datetime.now()

    # Check message 1
    retval1 = other.search(token1, msg_send1)['messages']
    assert retval1[0]['message_id'] == msg_id1
    assert retval1[0]['u_id'] == u_id1
    assert retval1[0]['message'] == msg_send1
    assert retval1[0]['time_created'] > time_before1
    assert retval1[0]['time_created'] < time_after1
    assert len(retval1) == 1

    # Send message 2
    msg_send2 = 'The quick brown dog jumps over the lazy fox'
    time_before2 = datetime.datetime.now()
    msg_id2 = message.message_send(token1, ch_id, msg_send2)['message_id']
    time_after2 = datetime.datetime.now()

    # Check message 2
    retval2 = other.search(token1, msg_send2)['messages']
    assert retval2[0]['message_id'] == msg_id2
    assert retval2[0]['u_id'] == u_id1
    assert retval2[0]['message'] == msg_send2
    assert retval2[0]['time_created'] > time_before2
    assert retval2[0]['time_created'] < time_after2
    assert len(retval2) == 1


# Stranger to channel sends a message to that channel
def test_message_send_stranger(get_new_user_1, get_new_user_2):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Register test user 2 (stranger)
    _, token2 = get_new_user_2

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
    _, token1 = get_new_user_1

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Actual test
    msg_send = ('T' * 1001)
    message.message_send(token1, ch_id, msg_send)
    with pytest.raises(error.InputError):
        message.message_send(token1, ch_id, msg_send)
