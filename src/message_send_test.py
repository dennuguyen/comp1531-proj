#Raymond: Tests on message_send()

import pytest
import message
import auth
import channel
import channels
import error
import message_test_helper

def test_send_by_authorised_user():

    #Setup
        #Register test user 1
    token = message_test_helper.get_new_user1()[1]

        #Create test channel 1
    channel_id = channels.channels_create(token, 'test_channel1', True)['channel_id']

    #Actual test
    msgsend = 'The quick brown fox jumps over the lazy dog'
    message_id = message.message_send(token, channel_id, message)['message_id']
    start = 0
    channel_messages_retval = channel.channel_messages(token, channel_id, start)
    assert channel_messages_retval['messages'][0]['message_id'] == message_id
    assert channel_messages_retval['messages'][0]['message'] == msgsend

    #Clean up (if necessary)

def test_send_non_member():
    #Setup
        #Register test user 1
    token = message_test_helper.get_new_user1()[1]

        #Create test channel 1
    channel_id = channels.channels_create(token, 'test_channel1', True)['channel_id']

        #Log out test user 1
    auth.auth_logout(token)

        #Register test user 2

    token2 = message_test_helper.get_new_user2()[1]

    #Actual test
    msg_tosend = 'The quick brown fox jumps over the lazy dog'
    with pytest.raises(error.AccessError):
        message.message_send(token2, channel_id, msg_tosend)

    #Clean up (if necessary)
    pass

def test_send_message_exceed_limit():
    
    #Setup
        #Register test user 1
    token = message_test_helper.get_new_user1()[1]

        #Create test channel 1
    channel_id = channels.channels_create(token, 'test_channel1', True)['channel_id']
    
    #Actual test
    msg_tosend = ('T'*1001)
    message.message_send(token, channel_id, message)
    with pytest.raises(error.InputError):
        message.message_send(token, channel_id, msg_tosend)

    #Clean up (if necessary)
    pass
