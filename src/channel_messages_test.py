import pytest
import channel
import error
import channels
import auth
import message

############## COMPLETE TEST FUNCTIONS BELOW ##################
 # if message length <= 50
def test_channel_messages_less_than_50(get_new_user_1):

    # set up environment
    _, token1 = get_new_user_1
    ch_id = channels.channels_create(token1, 'New Channel', True)['channel_id']

    # create dummy messages
    for i in range(5):
        msg = 'test message ' + str(i+1)
        message.message_send(token1, ch_id, msg)
        i += 1
  
    retval = channel.channel_messages(token1, ch_id, 0)
    
    assert len(retval['messages']) == 5
    assert retval['start'] == 0
    assert retval['end'] == -1 

# if messages length > 50
def test_channel_messages_greater_than_50(get_new_user_1):

    # set up environment
    _, token1 = get_new_user_1
    ch_id = channels.channels_create(token1, 'New Channel', True)['channel_id']

    for i in range(124):
        msg = 'test message ' + str(i+1)
        message.message_send(token1, ch_id, msg)
        i += 1

    retval = channel.channel_messages(token1, ch_id, 0)
    assert len(retval['messages']) == 50
    assert retval['start'] == 0
    assert retval['end'] == 50
    retval = channel.channel_messages(token1, ch_id, 50)
    assert len(retval['messages']) == 50
    assert retval['start'] == 50
    assert retval['end'] == 100 
    retval = channel.channel_messages(token1, ch_id, 100)
    assert len(retval['messages']) == 24
    assert retval['start'] == 100
    assert retval['end'] == -1 


def test_channel_messages_invalid_channel_id(get_new_user_1):

    # set up environment
    _, token1 = get_new_user_1
    ch_id = channels.channels_create(token1, 'New Channel', True)['channel_id']

    with pytest.raises(error.InputError):
        channel.channel_messages(token1, ch_id+1, 0)

def test_channel_messages_start_is_greater(get_new_user_1):

    _, token1 = get_new_user_1
    ch_id = channels.channels_create(token1, 'New Channel', True)

    for i in range(5):
        msg = 'test message ' + str(i+1)
        message.message_send(token1, ch_id, msg)
        i += 1

    with pytest.raises(error.InputError):
        channel.channel_messages(token1, ch_id, 10)

def test_channel_messages_unauthorised_user(get_new_user_1, get_new_user_2):   
    
    _, token1 = get_new_user_1 
    _, token2 = get_new_user_2

    ch_id = channels.channels_create(token1, 'New Channel', True)['channel_id']   

    with pytest.raises(error.AccessError):
        channel.channel_messages(token2, ch_id, 10)