import pytest, channels, error
from channels_list_test import create_example_list
from channel import channel_join
from auth import auth_register

# create an example list for use in test_list() and test_listall()
def create_example_list():
    channel_create(token, 'Channel1', True)
    channel_create(token, 'Channel2', True)
    channel_create(token, 'Channel3', True)
    channel_create(token, 'Channel4', True)

# calling listall() should return all channels with their details
def test_channels_listall():

    create_example_list()

    # create a user and give user some channel memberships
    u_id, token = auth_register('example@unsw.com', 'password', 'John', 'Doe')
    channel_join(token, 1)
    channel_join(token, 2)
    channel_join(token, 4)

    # valid token
    assert channels_listall(token) == 

    # no given token
    assert channel_list('') == {}


def test_channels_listall_invalid_token():
    # invalid token
    invalid_token = token + 1
    assert channel_list(invalid_token) == {}