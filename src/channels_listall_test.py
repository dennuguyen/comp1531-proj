import pytest, channel, auth, channels, error

def test_environment():

# Dummy information
    token = auth.auth_register('example@unsw.edu.au', 'qwert123', 'John', 'Doe' )['token']

# Create some channels
    ch_id1 = channels.channels_create(token, 'channel 1', True)
    ch_id2 = channels.channels_create(token, 'channel 2', True)
    ch_id3 = channels.channels_create(token, 'channel 3', True)
    ch_id4 = channels.channels_create(token, 'channel 4', True)

    return ch_id1, ch_id2, ch_id3, ch_id4, token

def test_channels_listall():

    token1 = test_environment()[4]
    ch_id1 = test_environment()[0]
    ch_id3 = test_environment()[2]

    token2 = auth.auth_register('example2@unsw.com', 'qwert246', 'Jaden', 'Smith')['token']

    channel.channel_join(token2, ch_id1)
    channel.channel_join(token2, ch_id3)

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

    # valid token
    assert channels.channels_listall(token1) == channels.channels_listall(token2) == test_list

def test_channels_invalid_token():

    token = test_environment()[4]

    # no given token
    assert channels.channels_listall('') == {}

    # invalid token
    
    invalid_token = token + 'a'
    assert channels.channels_listall(invalid_token) == {}

def test_channels_list_empty():
    token = auth.auth_register('example@unsw.com', 'password', 'Jaden', 'Smith')['token']
    assert channels.channels_listall(token) == {}
