#Raymond: Tests on message_edit()

import pytest
import message
import auth
import channel
import channels
import error
import message_test_helper


# User edits their own message
def test_message_edit():

    # Register test user 1 (owner)
    email1, password1, name_first1, name_last1 = message_test_helper.get_new_user1(
    )
    register_retval1 = auth.auth_register(email1, password1, name_first1,
                                          name_last1)
    u_id1, token1 = register_retval1['u_id'], register_retval1['token']

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Send message 1
    msg_send1 = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token1, ch_id, msg_send1)

    # Actual test
    msg_send2 = 'The quick brown dog jumps over the lazy fox.'
    message.message_edit(token1, msg_id, msg_send2)

    start = 0
    assert channel.channel_messages(
        token1, ch_id, start)['messages'][0]['message'] == msg_send2


# User edits another user's message
def test_message_edit_by_non_authorised_user():

    # Register test user 1 (owner)
    email1, password1, name_first1, name_last1 = message_test_helper.get_new_user1(
    )
    register_retval1 = auth.auth_register(email1, password1, name_first1,
                                          name_last1)
    u_id1, token1 = register_retval1['u_id'], register_retval1['token']

    # Register test user 2 (user)
    email2, password2, name_first2, name_last2 = message_test_helper.get_new_user2(
    )
    register_retval2 = auth.auth_register(email2, password2, name_first2,
                                          name_last2)
    u_id2, token2 = register_retval2['u_id'], register_retval2['token']

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']
    channel.channel_join(token2, ch_id)  # user2 joins as member

    # Send message 1
    msg_send1 = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token1, ch_id, msg_send1)

    # Actual test
    msg_send2 = 'The quick brown dog jumps over the lazy fox.'
    with pytest.raises(error.AccessError):
        message.message_edit(token2, msg_id, msg_send2)


# Channel owner can edit any message
def test_message_edit_by_owner():

    # Register test user 1 (owner)
    email1, password1, name_first1, name_last1 = message_test_helper.get_new_user1(
    )
    register_retval1 = auth.auth_register(email1, password1, name_first1,
                                          name_last1)
    u_id1, token1 = register_retval1['u_id'], register_retval1['token']

    # Register test user 2
    email2, password2, name_first2, name_last2 = message_test_helper.get_new_user2(
    )
    register_retval2 = auth.auth_register(email2, password2, name_first2,
                                          name_last2)
    u_id2, token2 = register_retval2['u_id'], register_retval2['token']

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']
    channel.channel_join(token2, ch_id)  # user2 joins as member

    # Send message 1
    msg_send1 = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token2, ch_id, msg_send1)

    #Actual test
    msg_send2 = 'The quick brown dog jumps over the lazy fox.'
    message.message_edit(token1, msg_id, msg_send2)
    start = 0
    assert channel.channel_messages(
        token2, ch_id, start)['messages'][0]['message'] == msg_send2


# Message edit is empty therefore must be removed
def test_message_edit_to_remove():

    # Register test user 1 (owner)
    email1, password1, name_first1, name_last1 = message_test_helper.get_new_user1(
    )
    register_retval1 = auth.auth_register(email1, password1, name_first1,
                                          name_last1)
    u_id1, token1 = register_retval1['u_id'], register_retval1['token']

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Send message 1
    msg_send1 = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token1, ch_id, msg_send1)

    #Actual test
    msg_send2 = ''
    message.message_edit(token1, msg_id, msg_send2)
    start = 0
    channel_messages_retval = channel.channel_messages(token1, ch_id, start)
    assert channel_messages_retval == {}