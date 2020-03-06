import pytest, error
import channels
import channel
import auth



def test_environment():

# Dummy information
    token = auth.auth_register('example@unsw.edu.au', 'qwert123', 'John', 'Doe' )['token']

# Create some channels
    ch_id1 = channels.channels_create(token, 'channel 1', True)
    ch_id2 = channels.channels_create(token, 'channel 2', True)
    ch_id3 = channels.channels_create(token, 'channel 3', True)
    ch_id4 = channels.channels_create(token, 'channel 4', True)

    return ch_id1, ch_id2, ch_id3, ch_id4, token


def test_channels_list_creator():

# Setup
    token = test_environment()[3]

    test_list = {
        'channels': [
        	{
        		'channel_id': ch_id1,
        		'name': 'channel 1',
        	},
            {
        		'channel_id': ch_id2,
        		'name': 'channel 2',
        	},
            {
        		'channel_id': ch_id3,
        		'name': 'channel 3',
        	},
            {
        		'channel_id': ch_id4,
        		'name': 'channel 4',
        	},
        ],
    }

# Actual test
    assert channels.channels_list(token) == test_list

def test_channels_list_member():

# Setup
    ch_id1 = test_environment()[0]
    ch_id2 = test_environment()[1]
    ch_id4 = test_environment()[3]

    token = auth.auth_register('example2@unsw.com', 'password', 'Jaden', 'Smith')['token']
    channel.channel_join(token, ch_id1)
    channel.channel_join(token, ch_id2)
    channel.channel_join(token, ch_id4)

    test_list = {
        'channels': [
        	{
        		'channel_id': ch_id1,
        		'name': 'channel 1',
        	},
            {
        		'channel_id': ch_id2,
        		'name': 'channel 2',
        	},
            {
        		'channel_id': ch_id4,
        		'name': 'channel 4',
        	},
        ],
    }

# Actual test
    assert channels.channels_list(token) == test_list

def test_channels_invalid_token():

# Setup
    token = test_environment()[3]

# Actual test
    assert channels.channels_list('') == {}

    invalid_token = token + 'a'
    assert channels.channels_list(invalid_token) == {}

def test_channels_list_empty():

#Setup  
    token = auth.auth_register('example@unsw.com', 'password', 'Jaden', 'Smith')['token']
    
#Actual test
    assert channels.channels_list(token) == {}




