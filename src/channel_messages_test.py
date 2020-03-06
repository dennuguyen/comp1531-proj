import pytest
import channel
import error
import channels
import auth

def test_environment():
    u_id1, token1 = auth.auth_register('example@unsw.com', 'password', 'The', 'User')
    u_id2, token2 = auth.auth_register('owner@unsw.com', 'password', 'The', 'Owner')
    u_id3, token3 = auth.auth_register('stranger@unsw.com', 'password', 'A', 'Stranger')

    return u_id1, token1, u_id2, token2, u_id3, token3, ch_id


############## COMPLETE TEST FUNCTIONS BELOW ##################
def test_channel_messages_less_than_50():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
    ch_id = channels.channels_create(token1, 'New Channel', True)

    # add some messages to the channel
    # if message length <= 50

    for integer in range(1,6):
        message = 'test message ' + f'{integer}'
        message_send(token1, ch_id, message)
        integer += 1

    retval = channel.channel.messages(token1, ch_id, 0)
    for msg in retval['messages']:
        no_msg += 1

    assert no_msg = 5
    assert retval['start'] = 0
    assert retval['end'] = -1 


def test_channel_messages_greater_than_50():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
    ch_id = channels.channels_create(token1, 'New Channel', True)

    # if messages length > 50

    for integer in range(1,56):
        message = 'test message ' + f'{integer}'
        message_send(token1, ch_id, message)
        integer += 1

    retval = channel.channel.messages(token1, ch_id, 0)
    for msg in retval['messages']:
        no_msg += 1

    assert no_msg = 50
    assert retval['start'] = 0
    assert retval['end'] = 50 

def test_channel_messages_invalid_channel_id():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
    ch_id = channels.channels_create(token1, 'New Channel', True)

    with pytest.raises(error.InputError):
        channel_messages(token1, ch_id+1, 0)

def test_channel_messages_start_is_greater():

    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
    ch_id = channels.channels_create(token1, 'New Channel', True)

    for integer in range(1,6):
        message = 'test message ' + f'{integer}'
        message_send(token1, ch_id, message)
        integer += 1

    with pytest.raises(error.InputError):
        channel.channel_messages(token1, ch_id, 10)

def test_channel_messages_unauthorised_user():
    
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
    ch_id = channels.channels_create(token1, 'New Channel', True)   

    with pytest.raises(error.AccessError):
        channel.channel_messages(token2, ch_id, 10)