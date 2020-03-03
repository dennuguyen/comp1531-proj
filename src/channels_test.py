# channels_test.py
# 
# 'channels' is a LIST of DICTIONARIES where each dictionary contains types
#   e.g. { channel_id, name }

import pytest, channels, error
from channel import channel_join
from auth import auth_register

# create an example list for use in test_list() and test_listall()
def create_example_list():
    example_list = {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	},
            {
        		'channel_id': 2,
        		'name': 'Hello',
        	},
            {
        		'channel_id': 3,
        		'name': 'Welcome',
        	},
            {
        		'channel_id': 4,
        		'name': '4th Channel',
        	},
        ],
    }

    auth_list = {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	},
            {
        		'channel_id': 2,
        		'name': 'Hello',
        	},
            {
        		'channel_id': 4,
        		'name': '4th Channel',
        	},
        ],
    }

    return example_list, auth_list


# test successful channel creation
def test_channels_list():

    example_list, auth_list = create_example_list()

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
    assert list('') == {}

    # invalid token
    invalid_token = token + 1
    assert list(invalid_token) == {}


def test_channels_create():
    # creating a channel should return a unique channel id
    assert channels_create('123', 'My Channel', True) == 1

    # making new channel
    assert channels_create('123', 'My Second Channel', False) == 2

    # making channel with same name
    with pytest.raises(InputError):
        channels_create('123', 'My Channel', True)

    # making channel with same name but with different token
    with pytest.raises(InputError):
        channels_create('1', 'My Channel', True)

    # making channel with same name but with different permissions
    with pytest.raises(InputError):
        channels_create('123', 'My Channel', False)

    # making a channel with empty name
    with pytest.raises(InputError):
        channels_create('123', '', False)

    # making a channel with only whitespace name
    with pytest.raises(InputError):
        channels_create('123', ' ', True)

    # channel name limited to 20 characters long
    assert channels_create('123', '01234567890123456789', True)

    with pytest.raises(InputError):
        channels_create('123', '0123456789 0123456789', True)
