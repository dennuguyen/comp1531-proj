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
