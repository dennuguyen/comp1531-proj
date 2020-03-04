import pytest, channels, error
from channel import channel_join
from auth import auth_register

# function to create test environment
def test_environment():
    u_id, token = auth_register('example@unsw.com', 'password', 'John', 'Doe')

    return u_id, token

def test_channels_create():
    u_id, token = test_environment()

    # creating a channel should return a unique channel id
    assert channels_create(token, 'My Channel', True) == 1

def test_channels_create_more():
    u_id, token = test_environment()

    # making new channel
    assert channels_create(token, 'My Second Channel', False) == 2

    # making channel with same name
    assert channels_create(token, 'My Second Channel', True) == 3

def test_channels_create_other():
    u_id, token = test_environment()

    # making a channel with empty name
    assert channels_create(token, '', False) == 4

    # making a channel with only whitespace name
    assert channels_create(token, ' ', True) == 5

def test_channels_create_invalid_token():
    u_id, token = test_environment()

    # making channel with same name but with invalid token
    with pytest.raises(InputError):
        channels_create('1', 'My Channel', True)

def test_channels_create_name_max_length():
    u_id, token = test_environment()

    # channel name limited to 20 characters long
    assert channels_create(token, '01234567890123456789', True)

    with pytest.raises(InputError):
        channels_create(token, '0123456789 0123456789', True)
