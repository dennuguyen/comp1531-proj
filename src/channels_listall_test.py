import pytest, channels, error
from channel import channel_join
from auth import auth_register

def test_environment():

    # dummy information
    token = '123'
    channel1 = 'Channel 1'
    channel2 = 'Channel 2'
    channel3 = 'Channel 3'
    channel4 = 'Channel 4'

    # create some channels
    ch_id1 = channels_create(token, channel1, True)
    ch_id2 = channels_create(token, channel2, True)
    ch_id3 = channels_create(token, channel3, True)
    ch_id4 = channels_create(token, channel4, True)

    # create a list for comparison
    example_list = {
        'channels': [
        	{
        		'channel_id': ch_id1,
        		'name': channel1,
        	},
            {
        		'channel_id': ch_id2,
        		'name': channel2,
        	},
            {
        		'channel_id': ch_id3,
        		'name': channel3,
        	},
            {
        		'channel_id': ch_id4,
        		'name': channel4,
        	},
        ],
    }

    return ch_id1, ch_id2, ch_id3, ch_id4, example_list

# calling listall() should return all channels with their details
def test_channels_listall():

    ch_id1, ch_id2, ch_id3, ch_id4, example_list = test_environment()

    # create a user and give user some channel memberships
    u_id, token = auth_register('example@unsw.com', 'password', 'John', 'Doe')
    channel_join(token, ch_id1)
    channel_join(token, ch_id3)

    # valid token
    assert channels_listall(token) == example_list

    # no given token
    assert channel_list('') == {}

    # invalid token
    invalid_token = token + 1
    assert channel_list(invalid_token) == {}
