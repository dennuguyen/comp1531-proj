import pytest
from channel import channel_invite, channel_addowner
from error import *
from channels import channels_create
from auth import auth_register

def test_environment():
    u_id1, token1 = auth_register('example@unsw.com', 'password', 'The', 'User')
    u_id2, token2 = auth_register('owner@unsw.com', 'password', 'The', 'Owner')
    ch_id = channels_create(token, 'New Channel', True)

    return u_id1, token1, u_id2, token2, ch_id

def test_channel_invite():

    # set up environment
    u_id1, token1, u_id2, token2, ch_id = test_environment()
    channel_addowner(token2, ch_id)

    # The owner invites the user to new channel
    assert channel_invite(token2, ch_id, u_id1) == {}

    # The owner invites themself to new channel
    assert channel_invite(token2, ch_id, u_id2) == {}

    # The owner re-invites the user who is already member
    assert channel_invite(token2, ch_id, u_id1) == {}

    # The user invites the owner to new channel
    with pytest.raises(AccessError):
        channel_invite(token1, ch_id, u_id2)

    # The user invites themself to new channel
    with pytest.raises(AccessError):
        channel_invite(token1, ch_id, u_id1)

    # invalid channel id i.e. channel does not exist
    with pytest.raises(InputError):
        channel_invite(token2, ch_id + 1, u_id1)

    # invalid user id i.e. user does not exist
    with pytest.raises(InputError):
        channel_invite(token, ch_id, u_id + 1)
