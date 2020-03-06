import pytest, channels, channel, auth, error

def test_environment():

# Dummy information
    token = auth.auth_register('example@unsw.edu.au', 'qwert123', 'John', 'Doe' )['token']

# Create some channels
    ch_id1 = channels.channels_create(token, 'channel 1', True)['channel_id']

    return ch_id1, token

def test_channels_create_public():

#Setup
    ch_id, token = test_environment()


# Actual test
    assert ch_id == channels.channels_listall(token)['channels'][0]['channel_id']

def test_channels_create_private():

# Setup
    token = test_environment()[1]

    # creating a channel should return a unique channel id
    ch_id = channels.channels_create(token, 'My Channel', False)['channel_id']
    
# Actual test
    assert ch_id == channels.channels_listall(token)['channels'][0]['channel_id']

def test_channels_create_multiple():

# Setup
    token = test_environment()[1]
    ch_id1 = channels.channels_create(token, 'My Second Channel', False)['channel_id']
    ch_id2 = channels.channels_create(token, 'My Second Channel', False)['channel_id']

# Actual test
    assert channels.channels_listall(token)['channels'][0]['channel_id'] == ch_id1
    assert channels.channels_listall(token)['channels'][1]['channel_id'] == ch_id2

def test_channels_create_invalid_token():
    token = test_environment()[1]
    invalid_token = token + 'a'

    with pytest.raises(error.InputError):
        channels.channels_create(invalid_token, 'My Channel', True)

def test_channels_create_invalid_name():

# Setup
    token = test_environment()[1]

# Actual test
    # Making a channel with empty name
    assert channels.channels_create(token, '', False)['channel_id'] != channels.channels_listall(token)['channels'][1]['channel_id']
    assert channels.channels_create(token, '', False) == {}

    # Making a channel with only whitespace name
    assert channels.channels_create(token, ' ', False)['channel_id'] != channels.channels_listall(token)['channels'][1]['channel_id']
    assert channels.channels_create(token, ' ', False) == {}
    # Making a channel with word exceeding limit
    with pytest.raises(error.InputError):
        channels.channels_create(token, '0123456789 0123456789', True)
