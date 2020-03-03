# channels_test.py
# 
# 'channels' is a LIST of DICTIONARIES where each dictionary contains types
#   e.g. { channel_id, name }

import pytest, channels, error

# test successful channel creation
def test_list():

    example_dict = {
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
        		'name': '',
        	},
        ],
    }

    auth_dict = {
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
        		'name': '',
        	},
        ],
    }

    # valid token
    assert listall('123') == auth_dict
    assert listall('123') != example_dict

    # no given token
    assert list('') == None

    # invalid token
    assert list('321') == None


# calling listall() should return all channels with their details
def test_listall():

    # where is the data structure for the channel held?
    example_dict = {
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
        		'name': '',
        	},
        ],
    }

    # valid token
    assert listall('123') == example_dict

    # no given token
    assert list('') == None

    # invalid token
    assert list('321') == None


def test_create_channel():
    # creating a channel should return a unique channel id
    assert create('123', 'My Channel', True) == 1

    # making new channel
    assert create('123', 'My Second Channel', False) == 2

    # making channel with same name
    with pytest.raises(InputError):
        create('123', 'My Channel', True)

    # making channel with same name but with different token
    with pytest.raises(InputError):
        create('1', 'My Channel', True)

    # making channel with same name but with different permissions
    with pytest.raises(InputError):
        create('123', 'My Channel', False)

    # making a channel with empty name
    with pytest.raises(InputError):
        create('123', '', False)

    # making a channel with only whitespace name
    with pytest.raises(InputError):
        create('123', ' ', True)

    # channel name limited to 20 characters long
    assert create('123', '01234567890123456789', True)

    with pytest.raises(InputError):
        create('123', '0123456789 0123456789', True)

