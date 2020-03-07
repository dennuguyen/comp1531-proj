import pytest
import message
import auth
import channel
import channels
import error
import message_test_helper


# Test user removing own message
def test_remove_message_user():

    # Register test user 1
    u_id, token = message_test_helper.get_new_user1()
    register_retval = auth.auth_register(email, password, name_first,
                                         name_last)

    # Create test channel 1
    ch_id = channels.channels_create(token, 'test_channel1',
                                     True)['channel_id']

    # Send message 1
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    message_id = message.message_send(token, ch_id, msg_send)

    # Actual test
    message.message_remove(token, message_id)
    start = 0
    channel_messages_retval = channel.channel_messages(token, channel_id,
                                                       start)
    assert channel_messages_retval == {}


# Test owner removing user message
def test_remove_message_user():

    # Register test user 1
    u_id, token = message_test_helper.get_new_user1()

    # Create test channel 1
    ch_id = channels.channels_create(token, 'test_channel1',
                                     True)['channel_id']

    # Send message 1
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    message_id = message.message_send(token, ch_id, msg_send)

    # Actual test
    message.message_remove(token, message_id)
    start = 0
    channel_messages_retval = channel.channel_messages(token, channel_id,
                                                       start)
    assert channel_messages_retval == {}


def test_remove_non_existing_message():
    #Setup
    #Register test user 1
    token = message_test_helper.get_new_user1()[1]

    #Create test channel 1
    channel_id = channels.channels_create(token, 'test_channel1',
                                          True)['channel_id']

    #Send message 1
    msgsend = 'The quick brown fox jumps over the lazy dog.'
    message_id = message.message_send(token, channel_id, msgsend)

    #Remove message 1
    message.message_remove(token, message_id)

    #Actual test
    with pytest.raises(error.InputError):
        message.message_remove(token, message_id)

    #Clean up (if necessary)
    pass


def test_remove_non_authorised_user():
    #Setup
    #Register test user 1
    token = message_test_helper.get_new_user1()[1]

    #Create test channel 1
    channel_id = channels.channels_create(token, 'test_channel1',
                                          True)['channel_id']

    #Send message 1
    msgsend = 'The quick brown fox jumps over the lazy dog.'
    message_id = message.message_send(token, channel_id, msgsend)

    auth.auth_logout(token)

    #Register test user 2
    token2 = message_test_helper.get_new_user2()[1]

    #Invite test user 2 to test channel 1
    channel.channel_join(token2, channel_id)

    #Actual test
    with pytest.raises(error.AccessError):
        message.message_remove(token2, message_id)

    #Clean up (if necessary)
    pass