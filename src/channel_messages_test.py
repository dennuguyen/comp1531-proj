import pytest
import channel
import error
import channels
import auth

def get_new_user_1():
    email = 'john_doe@unsw.edu.au'
    password = 'password'
    name_first = 'John'
    name_last = 'Doe'
    return email, password, name_first, name_last


def get_new_user_2():
    email = 'hugh_jackman@unsw.edu.au'
    password = 'password'
    name_first = 'Hugh'
    name_last = 'Jackman'
    return email, password, name_first, name_last


def get_new_user_3():
    email = 'ted_bundy@unsw.edu.au'
    password = 'password'
    name_first = 'Ted'
    name_last = 'Bundy'
    return email, password, name_first, name_last


def get_channel_name():
    ch_name = 'New Channel'
    return ch_name


# check mess
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