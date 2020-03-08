#Raymond: Tests on message_send()

import pytest
import message
import auth
import channel
import channels
import error
import message_test_helper


# User sends a message to a channel they are a member of
def test_message_send_member():

    # Register test user 1 (owner)
    email1, password1, name_first1, name_last1 = message_test_helper.get_new_user1(
    )
    register_retval1 = auth.auth_register(email1, password1, name_first1,
                                          name_last1)
    u_id1, token1 = register_retval1['u_id'], register_retval1['token']

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
def test_message_send_stranger():

    # Register test user 1 (owner)
    email1, password1, name_first1, name_last1 = message_test_helper.get_new_user1(
    )
    register_retval1 = auth.auth_register(email1, password1, name_first1,
                                          name_last1)
    u_id1, token1 = register_retval1['u_id'], register_retval1['token']

    # Register test user 2 (stranger)
    email2, password2, name_first2, name_last2 = message_test_helper.get_new_user2(
    )
    register_retval2 = auth.auth_register(email2, password2, name_first2,
                                          name_last2)
    u_id2, token2 = register_retval2['u_id'], register_retval2['token']

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Actual test
    msg_send = 'The quick brown fox jumps over the lazy dog'
    with pytest.raises(error.AccessError):
        message.message_send(token2, ch_id, msg_send)


# Message is more than 1000 char
def test_message_send_1000_char():

    # Register test user 1 (owner)
    email1, password1, name_first1, name_last1 = message_test_helper.get_new_user1(
    )
    register_retval1 = auth.auth_register(email1, password1, name_first1,
                                          name_last1)
    u_id1, token1 = register_retval1['u_id'], register_retval1['token']

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Actual test
    msg_send = ('T' * 1001)
    message.message_send(token1, ch_id, msg_send)
    with pytest.raises(error.InputError):
        message.message_send(token1, ch_id, msg_send)
