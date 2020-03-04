import pytest, channels, error
from channel import channel_join
from auth import auth_register

def test_channels_create():
    # creating a channel should return a unique channel id
    assert channels_create('123', 'My Channel', True) == 1

def test_channels_create_more():
    # making new channel
    assert channels_create('123', 'My Second Channel', False) == 2

    # making channel with same name
    assert channels_create('123', 'My Channel', True) == 3

def test_channels_create_other():
    # making a channel with empty name
    assert channels_create('123', '', False) == 4

    # making a channel with only whitespace name
    assert channels_create('123', ' ', True) == 5

def test_channels_create_invalid_token():
    # making channel with same name but with invalid token
    with pytest.raises(InputError):
        channels_create('1', 'My Channel', True)

def test_channels_create_name_max_length():
    # channel name limited to 20 characters long
    assert channels_create('123', '01234567890123456789', True)

    with pytest.raises(InputError):
        channels_create('123', '0123456789 0123456789', True)
