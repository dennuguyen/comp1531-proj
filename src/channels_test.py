# channels_test.py
# 
# 'channels' is a LIST of DICTIONARIES where each dictionary contains types
#   e.g. { channel_id, name }

import pytest, channels, error
from channel import channel_join
from auth import auth_register

# create an example list for use in test_list() and test_listall()
def create_example_list():
    channel_create(token, 'Channel1', True)
    channel_create(token, 'Channel2', True)
    channel_create(token, 'Channel3', True)
    channel_create(token, 'Channel4', True)


# test successful channel creation
def test_channels_list():

    create_example_list()

    # create a user and give user some channel memberships
    u_id, token = auth_register('example@unsw.com', 'password', 'John', 'Doe')
    channel_join(token, 1)
    channel_join(token, 2)
    channel_join(token, 4)

    # valid token
    assert channels_list(token) == auth_list
    assert channels_list(token) != example_list

    # no given token
    assert channels_list('') == {}

    # invalid token
    invalid_token = token + 1
    assert channels_list(invalid_token) == {}


# calling listall() should return all channels with their details
def test_channels_listall():

    example_list, auth_list = create_example_list()

    # create a user and give user some channel memberships
    u_id, token = auth_register('example@unsw.com', 'password', 'John', 'Doe')
    channel_join(token, 1)
    channel_join(token, 2)
    channel_join(token, 4)

    # valid token
    assert channels_listall(token) == example_list
    assert channels_listall(token) != auth_list

    # no given token
    assert channel_list('') == {}

    # invalid token
    invalid_token = token + 1
    assert channel_list(invalid_token) == {}


def test_channels_create():
    # creating a channel should return a unique channel id
    assert channels_create('123', 'My Channel', True) == 1

    # making new channel
    assert channels_create('123', 'My Second Channel', False) == 2

    # making channel with same name
    assert channels_create('123', 'My Channel', True) == 3

    # making channel with same name but with invalid token
    with pytest.raises(InputError):
        channels_create('1', 'My Channel', True)

    

    # channel name limited to 20 characters long
    assert channels_create('123', '01234567890123456789', True)

    with pytest.raises(InputError):
        channels_create('123', '0123456789 0123456789', True)

def test_channels_invalid_token():

def test_channels_other():
    # making a channel with empty name
    assert channels_create('123', '', False) == 4

    # making a channel with only whitespace name
    assert channels_create('123', ' ', True) == 5