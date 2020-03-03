#Raymond: tests for message.py

import pytest
import message
import auth
import channels

#Tests for message_send

def test_send_by_authorised_user():
    #Setup
        #Register test user 1
    email = 'z1234567@student.unsw.edu.au'
    password = 'Qwert123'
    name_first = 'James'
    name_last = 'Bond'
    register_retval = auth.register(email, password, name_first, name_last)
    user_id = register_retval'[u_id]
    token = register_retval['token']
        #Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.create(token, channel_name, True )

    #Actual test
    message = 'The quick brown fox jumps over the lazy dog'
    message.send(token, channel_id, message)
    start = 0
    channel_message = channel.messages(token, channel_id, start)
    assert channel_message['messages'][0] == messages

    #Clean up (if necessary)
    pass

def test_send_non_member():
    #Setup
        #Register test user 1
    email = 'z0000001@student.unsw.edu.au'
    password = 'Qwert001'
    name_first = 'James'
    name_last = 'Bond'
    register_retval = auth.register(email, password, name_first, name_last)
    user_id = register_retval'[u_id]
    token = register_retval['token']
        #Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.create(token, channel_name, True )
    
        #Log out test user 1
    logout(token)

        #Register test user 2
    email = 'z000002@student.unsw.edu.au'
    password = 'Qwert002'
    name_first = 'John'
    name_last = 'Wick'
    register_retval = auth.register(email, password, name_first, name_last)
    user_id = register_retval'[u_id]
    token = register_retval['token']   

    #Actual test
    message = 'The quick brown fox jumps over the lazy dog'
    message.send(token, channel_id, message)
    with pytest.raises(AccessError):
        message.send(token, channel_id, message)

    #Clean up (if necessary)
    pass

def test_send_message_exceed_limit():
    #Setup
        #Register test user 1
    email = 'z0000001@student.unsw.edu.au'
    password = 'Qwert001'
    name_first = 'James'
    name_last = 'Bond'
    register_retval = auth.register(email, password, name_first, name_last)
    user_id = register_retval'[u_id]
    token = register_retval['token']
        #Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.create(token, channel_name, True )
    
    #Actual test
    message = 'Inquietude simplicity terminated she compliment remarkably few her nay. The weeks are ham asked jokes. Neglected perceived shy nay concluded. Not mile draw plan snug next all. Houses latter an valley be indeed wished merely in my. Money doubt oh drawn every or an china. Visited out friends for expense message set eat. Allow miles wound place the leave had. To sitting subject no improve studied limited. Ye indulgence unreserved connection alteration appearance my an astonished. Up as seen sent make he they of. Her raising and himself pasture believe females. Fancy she stuff after aware merit small his. Charmed esteems luckily age out. Of resolve to gravity thought my prepare chamber so. Unsatiable entreaties collecting may sympathize nay interested instrument. If continue building numerous of at relation in margaret. Lasted engage roused mother an am at. Other early while if by do to. Missed living excuse as be. Cause heard fat above first shall for. My smiling to he removal weather on anxious. Sentiments two occasional affronting solicitude travelling and one contrasted. Fortune day out married parties. '
    message.send(token, channel_id, message)
    with pytest.raises(InputError):
        message.send(token, channel_id, message)

    #Clean up (if necessary)
    pass

#Tests for message_remove

def test_remove_existing_message():
    
    pass

def test_remove_non_existing_message():
    
    pass

def test_remove_non_authorised_user():
    
    pass

#Tests for message_edit

def test_edit1():
    
    pass


