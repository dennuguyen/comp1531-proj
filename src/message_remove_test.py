import pytest
import message
import auth
import channel
import channels
import error
import message_test_helper


# Test user removing own message
def test_message_remove_message_user():

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

    # User sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token2, ch_id, msg_send)

    # Actual test
    message.message_remove(token2, msg_id)
    start = 0
    channel_messages_retval = channel.channel_messages(token, ch_id, start)
    assert channel_messages_retval == {}


# Test owner removing user message
def test_message_remove_message_owner():

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

    # User sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token2, ch_id, msg_send)

    # Actual test
    message.message_remove(token1, msg_id)
    start = 0
    channel_messages_retval = channel.channel_messages(token, ch_id, start)
    assert channel_messages_retval == {}


# Test InputError case
def test_message_remove_input_error():

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

    # User sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token2, ch_id, msg_send)

    # Testing message removal in empty channel
    message.message_remove(token1, msg_id)
    with pytest.raises(error.InputError):
        message.message_remove(token, msg_id)


# Test AccessError case
def test_message_remove_access_error():
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

    # Owner sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token1, ch_id, msg_send)

    # User tries to remove owner's message
    with pytest.raises(error.AccessError):
        message.message_remove(token2, msg_id)