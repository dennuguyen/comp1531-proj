import pytest
from channel import channel_invite
from error import *
from channels import channels_create
from auth import auth_register

def test_environment():
    u_id1, token1 = auth_register('example@unsw.com', 'password', 'The', 'User')
    u_id2, token2 = auth_register('owner@unsw.com', 'password', 'The', 'Owner')
    u_id3, token3 = auth_register('stranger@unsw.com', 'password', 'A', 'Stranger')
    ch_id = channels_create(token2, 'New Channel', True) # u_id2 is owner

    return u_id1, token1, u_id2, token2, u_id3, token3, ch_id

def test_channel_invite_owner_cases():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()

    # The owner invites the user to new channel
    assert channel_invite(token2, ch_id, u_id1) == {}

    # The owner invites themself to new channel
    assert channel_invite(token2, ch_id, u_id2) == {}

    # The owner re-invites the user who is already member
    assert channel_invite(token2, ch_id, u_id1) == {}

def test_channel_invite_user_cases():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()

    # The user invites the owner to new channel
    assert channel_invite(token1, ch_id, u_id2) == {}

    # The user invites themself to new channel
    assert channel_invite(token1, ch_id, u_id1) == {}

    # The user invites a stranger to new channel
    assert channel_invite(token1, ch_id, u_id3) == {}

def test_channel_invite_stranger_cases():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
    u_id4, token4 = auth_register('strangerzzz@unsw.com', 'password', 'Two', 'Strangerzzz')

    # A stranger invites the owner to new channel
    with pytest.raises(AccessError):
        channel_invite(token3, ch_id, u_id2)

    # A stranger invites themself to new channel
    with pytest.raises(AccessError):
        channel_invite(token3, ch_id, u_id3)

    # A stranger invites the user to new channel
    with pytest.raises(AccessError):
        channel_invite(token3, ch_id, u_id1)

    # A stranger invites another stranger to new channel
    with pytest.raises(AccessError):
        channel_invite(token3, ch_id, u_id4)

def test_channel_invite_validity():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()

    # invalid channel id i.e. channel does not exist
    with pytest.raises(InputError):
        channel_invite(token2, ch_id + 1, u_id1)

    # invalid user id i.e. user does not exist
    with pytest.raises(InputError):
        channel_invite(token2, ch_id, u_id1 + u_id2 + u_id3)
