#Raymond: Tests on message_edit()

import pytest
import message
import auth
import channel
import channels
import error
import message_test_helper

def test_message_edit():

    #Setup
        #Register test user 1
    token = message_test_helper.get_new_user1()[1]

        #Create test channel 1
    channel_id = channels.channels_create(token, 'test_channel1', True)['channel_id']

        #Send message 1
    msg = 'The quick brown fox jumps over the lazy dog.'
    message_id = message.message_send(token, channel_id, msg)

    #Actual test
    newmsg = 'The quick brown dog jumps over the lazy fox.'
    message.message_edit(token, message_id, newmsg)

    start = 0
    assert channel.channel_messages(token, channel_id, start)['messages'][0]['message'] == newmsg    
    
    #Clean up (if necessary)

    pass

def test_message_edit_by_non_authorised_user():
    
    #Setup
        #Register test user 1
    token = message_test_helper.get_new_user1()[1]

        #Create test channel 1
    channel_id = channels.channels_create(token, 'test_channel1', True)['channel_id']

        #Send message 1
    msg = 'The quick brown fox jumps over the lazy dog.'
    message_id = message.message_send(token, channel_id, msg)
    pass

        #Log out test user 1
    auth.auth_logout(token)

    #Register test user 2
    token2 = message_test_helper.get_new_user2()[1]

    #Actual test

    newmsg = 'The quick brown dog jumps over the lazy fox.'
    with pytest.raises(error.AccessError):
       message.message_edit(token2, message_id, newmsg)    
  
    #Clean up (if necessary)

    pass

def test_message_edit_by_owner():

    #Setup
        #Register test user 1
    token = message_test_helper.get_new_user1()[1]

        #Create test channel 1
    channel_id = channels.channels_create(token, 'test_channel1', True)['channel_id']

        #Register test user 2
    token2 = message_test_helper.get_new_user2()[1]

        #Test user 2 join test channel

    channel.channel_join(token2, channel_id)

        #Send message 1
    msg = 'The quick brown fox jumps over the lazy dog.'
    message_id = message.message_send(token2, channel_id, msg)

    #Actual test
    newmsg = 'The quick brown dog jumps over the lazy fox.'
    message.message_edit(token, message_id, newmsg)
    start = 0
    assert channel.channel_messages(token2, channel_id, start)['messages'][0]['message'] == newmsg    
    
    #Clean up (if necessary)
    pass

    