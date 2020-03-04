#Raymond: Tests on message_send()

import pytest
import message
import auth
import channels

def test_send_by_authorised_user():
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

    #Actual test
    message = 'The quick brown fox jumps over the lazy dog'
    message_id = message.message_send(token, channel_id, message)
    start = 0
    channel_messages_retval = channel.channel_messages(token, channel_id, start)
    assert channel_messages_retval['messages'][0]['message_id'] == 1
    assert channel_messages_retval['messages'][0]['message'] == message

    #Clean up (if necessary)

def test_send_non_member():
    #Setup

        #Register test user 1
    email = 'z0000001@student.unsw.edu.au'
    password = 'Qwert001'
    name_first = 'James'
    name_last = 'Bond'
    register_retval = auth.auth_register(email, password, name_first, name_last)
    user_id = register_retval['u_id']
    token = register_retval['token']

        #Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token, channel_name, True )
    
        #Log out test user 1
    logout(token)

        #Register test user 2
    email = 'z000002@student.unsw.edu.au'
    password = 'Qwert002'
    name_first = 'John'
    name_last = 'Wick'
    register_retval = auth.auth_register(email, password, name_first, name_last)
    user_id = register_retval'[u_id]
    token = register_retval['token']   

    #Actual test
    message = 'The quick brown fox jumps over the lazy dog'
    message.message_send(token, channel_id, message)
    with pytest.raises(AccessError):
        message.message_send(token, channel_id, message)

    #Clean up (if necessary)
    pass

def test_send_message_exceed_limit():
    #Setup
        #Register test user 1
    email = 'z0000001@student.unsw.edu.au'
    password = 'Qwert001'
    name_first = 'James'
    name_last = 'Bond'
    register_retval = auth.auth_register(email, password, name_first, name_last)
    user_id = register_retval'[u_id]
    token = register_retval['token']

        #Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token, channel_name, True )
    
    #Actual test
    message = ('T'*1001)
    message.message_send(token, channel_id, message)
    with pytest.raises(InputError):
        message.message_send(token, channel_id, message)

    #Clean up (if necessary)
    pass