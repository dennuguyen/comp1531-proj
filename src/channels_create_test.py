import pytest, channels, error
from channel import channel_join
from auth import auth_register

# function to create test environment
def test_environment():
    u_id1, token1 = auth_register('example1@unsw.com', 'password', 'John', 'Doe')
    u_id2, token2 = auth_register('example2@unsw.com', 'password', 'Jack', 'Toe')

    return u_id1, token1, u_id2, token2

def test_channels_create_public():
    u_id1, token1, u_id2, token2 = test_environment()

    # creating a channel should return a unique channel id
    ch_id = channels_create(token1, 'My Channel', True)['channel_id']

    # test for correct channel id
    assert ch_id == 1

    # test for public channel
    assert channel_join(token2, ch_id) == {}

def test_channels_create_private():
    u_id1, token1, u_id2, token2 = test_environment()

    # creating a channel should return a unique channel id
    ch_id = channels_create(token1, 'My Channel', False)['channel_id']
    
    # test for correct channel id
    assert ch_id == 1

    # test for private channel
    with pytest.raises(AccessError):
        channel_join(token2, ch_id)

def test_channels_create_multiple():
    u_id1, token1, u_id2, token2 = test_environment()

    # test for creation of channels with the same name and unique id
    assert channels_create(token1, 'My Second Channel', False)['channel_id'] == 1
    assert channels_create(token1, 'My Second Channel', True)['channel_id'] == 2

def test_channels_create_other():
    u_id1, token1, u_id2, token2 = test_environment()

    # making a channel with empty name
    assert channels_create(token1, '', False)['channel_id'] == 1

    # making a channel with only whitespace name
    assert channels_create(token1, ' ', True)['channel_id'] == 2

def test_channels_create_invalid_token():
    u_id1, token1, u_id2, token2 = test_environment()

    with pytest.raises(InputError):
        channels_create(token1 + token2, 'My Channel', True)

def test_channels_create_name_max_length():
    u_id1, token1, u_id2, token2 = test_environment()

    # channel name limited to 20 characters long
    assert channels_create(token1, '01234567890123456789', True)['channel_id'] == 1

    with pytest.raises(InputError):
        channels_create(token1, '0123456789 0123456789', True)
