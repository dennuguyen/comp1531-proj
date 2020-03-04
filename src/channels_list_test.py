import pytest, channels, error
from channel import channel_join
from auth import auth_register

# create an example list for use in test_list() and test_listall()
def create_example_list():
    ch_id1 = channel_create(token, 'Channel1', True)
    ch_id2 = channel_create(token, 'Channel2', True)
    ch_id3 = channel_create(token, 'Channel3', True)
    ch_id4 = channel_create(token, 'Channel4', True)

    return ch_id1, ch_id2, ch_id3, ch_id4

# test successful channel creation
def test_channels_list():

    ch_id1, ch_id2, ch_id3, ch_id4 = create_example_list()

    # create a user and give user some channel memberships
    u_id, token = auth_register('example@unsw.com', 'password', 'John', 'Doe')
    channel_join(token, ch_id1)
    channel_join(token, ch_id2)
    channel_join(token, ch_id4)

    # valid token
    assert channels_list(token) == {[ch_id1, ch_id2, ch_id4]}

    # no given token
    assert channels_list('') == {}

    # invalid token
    invalid_token = token + 1
    assert channels_list(invalid_token) == {}
