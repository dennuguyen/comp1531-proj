import pytest, channel, error
from channels import channels_create
from auth import auth_register


def create_user_channel():
    u_id, token = auth_register('example@unsw.com', 'password', 'John', 'Doe')
    ch_id = channels_create(token, 'New Channel', True)

    return u_id, token, ch_id


def test_channel_invite():

    # create a user and channel
    u_id, token, ch_id = create_user_channel()

    # invite user to new channel
    with pytest.raises(AccessError):
        channel_invite(token, ch_id, u_id)

    # re-invite user to check if user is now a channel member
    assert channel_invite(token, ch_id, u_id) == {}

    # invalid channel id i.e. channel does not exist
    with pytest.raises(InputError):
        channel_invite(token, ch_id + 1, u_id)

    # invalid user id i.e. user does not exist
    with pytest.raises(InputError):
        channel_invite(token, ch_id, u_id + 1)


def test_channel_details():

    # create a user and channel
    u_id1, token1, ch_id = create_user_channel()
    u_id2, token2 = auth_register('max_is_cool@unsw.com', 'password', 'Max', 'Power')

    # invite John Doe to the channel
    channel_invite(token1, ch_id, u_id1)

    correct_detail = {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

    # call detail() as channel member
    assert channel_details(token1, ch_id) == correct_detail

    # call detail() as non-channel user
    assert channel_details(token2, ch_id) == correct_detail

    # invalid channel id
    with pytest.raises(InputError):
        channel_details(token1, ch_id + 1)

    # invalid user id
    with pytest.raises(InputError):
        channel_details(token1 + token2, ch_id)


def test_channel_messages():

    # create a user and channel
    u_id, token, ch_id = create_user_channel()
    channel_invite(token, ch_id, u_id) # add user to channel

    # add some messages to the channel

    # if message length <= 50


    # if messages length > 50

    # no new messages
    assert channel_details(token, ch_id) == -1

    # start is greater than total number of msgs
    with pytest.raises

    # invalid channel id
    with pytest.raises(InputError):
        channel_details(token1, ch_id + 1)

    # invalid user id
    with pytest.raises(AccessError):
        channel_details(token1 + token2, ch_id)


def test_channel_leave():
    # leave('123', 1) == 
    assert details('123', 1)

def test_channel_join():

def test_channel_addowner():

def test_channel_removeowner():
