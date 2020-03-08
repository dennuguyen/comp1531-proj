import pytest, error
import channels
import channel
import auth

def test_channels_list_creator(get_new_user_1, get_channel_name_1, get_channel_name_2, get_channel_name_3, get_channel_name_4):

# Setup
    token = get_new_user_1[1]
    ch_id1 = channels.channels_create(token, get_channel_name_1, True)
    ch_id2 = channels.channels_create(token, get_channel_name_2, True)
    ch_id3 = channels.channels_create(token, get_channel_name_3, True)
    ch_id4 = channels.channels_create(token, get_channel_name_4, True)

    test_list = {
        'channels': [
        	{
        		'channel_id': ch_id1,
        		'name': get_channel_name_1,
        	},
            {
        		'channel_id': ch_id2,
        		'name': get_channel_name_2,
        	},
            {
        		'channel_id': ch_id3,
        		'name': get_channel_name_3,
        	},
            {
        		'channel_id': ch_id4,
        		'name': get_channel_name_4,
        	},
        ],
    }

# Actual test
    assert channels.channels_list(token) == test_list

def test_channels_list_member(get_new_user_1, get_channel_name_1, get_channel_name_2, get_channel_name_4):

# Setup
    token = get_new_user_1[1]
    ch_id1 = channels.channels_create(token, get_channel_name_1, True)
    ch_id2 = channels.channels_create(token, get_channel_name_2, True)
    ch_id4 = channels.channels_create(token, get_channel_name_4, True)

    
    channel.channel_join(token, ch_id1)
    channel.channel_join(token, ch_id2)
    channel.channel_join(token, ch_id4)

    test_list = {
        'channels': [
        	{
        		'channel_id': ch_id1,
        		'name': 'get_channel_name_1',
        	},
            {
        		'channel_id': ch_id2,
        		'name': 'get_channel_name_2',
        	},
            {
        		'channel_id': ch_id4,
        		'name': 'get_channel_name_4',
        	},
        ],
    }

# Actual test
    assert channels.channels_list(token) == test_list

def test_channels_invalid_token(get_new_user_1):

# Setup
    token = get_new_user_1[1]

# Actual test
    assert channels.channels_list('') == {}

    invalid_token = token + 'a'
    assert channels.channels_list(invalid_token) == {}

def test_channels_list_empty(get_new_user_1):

#Setup  
    token = get_new_user_1[1]
    
#Actual test
    assert channels.channels_list(token) == {}




