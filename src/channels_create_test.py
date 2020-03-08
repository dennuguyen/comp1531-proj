import pytest, channels, channel, auth, error

def test_channels_create_public(get_new_user_1):

#Setup
    token = get_new_user_1[1]
    ch_id = channels.channels_create(token, 'channel 1', True)['channel_id']

# Actual test
    flag = False
    for channel in channels.channels_listall(token)['channels']:
        if(channel['channel_id'] == ch_id):
            flag = True
    assert flag == True

def test_channels_create_private(get_new_user_1):

# Setup
    token = get_new_user_1[1]
    # creating a channel should return a unique channel id
    ch_id = channels.channels_create(token, 'My Channel', False)['channel_id']
    
# Actual test
    flag = False
    for channel in channels.channels_listall(token)['channels']:
        if(channel['channel_id'] == ch_id):
            flag = True
    assert flag == True

def test_channels_create_multiple(get_new_user_1):

# Setup
    token = get_new_user_1[1]
    ch_id1 = channels.channels_create(token, 'My Second Channel', False)['channel_id']
    ch_id2 = channels.channels_create(token, 'My Second Channel', False)['channel_id']

# Actual test
    flag1, flag2 = False, False
    for channel in channels.channels_listall(token)['channels']:
        if(channel['channel_id'] == ch_id1):
            flag1 = True
        if(channel['channel_id'] == ch_id2):
            flag2 = True
    assert flag1 == True and flag2 == True

def test_channels_create_invalid_token(get_new_user_1):
    token = get_new_user_1[1]
    invalid_token = token + 'a'

    with pytest.raises(error.InputError):
        channels.channels_create(invalid_token, 'My Channel', True)

def test_channels_create_invalid_name(get_new_user_1):

# Setup
    token = get_new_user_1[1]

# Actual test
    # Making a channel with empty name
    flag = False
    for channel in channels.channels_listall(token)['channels']:
        if(channel['channel_id'] == channels.channels_create(token, '', False)['channel_id']):
            flag = True
    assert flag == False
    assert channels.channels_create(token, '', False) == {}

    # Making a channel with only whitespace name
    flag = False
    for channel in channels.channels_listall(token)['channels']:
        if(channel['channel_id'] == channels.channels_create(token, '', False)['channel_id']):
            flag = True
    assert flag == False
    assert channels.channels_create(token, ' ', False) == {}
    # Making a channel with word exceeding limit
    with pytest.raises(error.InputError):
        channels.channels_create(token, '0123456789 0123456789', True)