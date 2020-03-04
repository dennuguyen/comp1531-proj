#Raymond: Tests on message_remove()

import pytest
import message
import auth
import channels

def test_remove_existing_message():
    #Setup
        #Register test user 1
    email = 'z1234567@student.unsw.edu.au'
    password = 'Qwert123'
    name_first = 'James'
    name_last = 'Bond'
    register_retval = auth.auth_register(email, password, name_first, name_last)
    user_id = register_retval['u_id']
    token = register_retval['token']

        #Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token, channel_name, True )
        
        #Send message 1
    message = 'The quick brown fox jumps over the lazy dog.'
    message_id = message.message_send(token, channel_id, message)

    #Actual test
    message_remove(token, message_id)
    start = 0
    channel_messages_retval = channel_messages(token, channel_id, start)
    assert channel_messages_retval == {}

    #Clean up(if necessary)
    pass

def test_remove_non_existing_message():
    
    pass

def test_remove_non_authorised_user():
    
    pass