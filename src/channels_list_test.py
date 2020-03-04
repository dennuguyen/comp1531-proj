import pytest, error
from channels import *
from channel import channel_join
from auth import auth_register

# create an example list for use in test_list() and test_listall()
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
        		'channel_id': ch_id4,
        		'name': channel4,
        	},
        ],
    }

    return ch_id1, ch_id2, ch_id3, ch_id4, example_list

# test successful channel creation
def test_channels_list():

    ch_id1, ch_id2, ch_id3, ch_id4, example_list = test_environment()

    # create a user and give user some channel memberships
    u_id, token = auth_register('example@unsw.com', 'password', 'John', 'Doe')
    channel_join(token, ch_id1)
    channel_join(token, ch_id2)
    channel_join(token, ch_id4)

    # valid token
    assert channels_list(token) == example_list

    # no given token
    assert channels_list('') == {}

    # invalid token
    invalid_token = token + 1
    assert channels_list(invalid_token) == {}
