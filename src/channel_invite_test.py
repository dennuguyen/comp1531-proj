import pytest
from channel import channel_invite
from error import *
from channels import channels_create
from auth import auth_register

@pytest.fixture(scope="module")
def test_environment(get_new_user_1, get_new_user_2, get_new_user_3):

    u_id1, token1 = get_new_user_3
    u_id2, token2 = get_new_user_2
    u_id3, token3 = get_new_user_1
    ch_id = channels_create(token2, 'New Channel', True) # u_id2 is owner

    return u_id1, token1, u_id2, token2, u_id3, token3, ch_id

def test_channel_invite_owner_cases(test_environment):

    # set up environment
    u_id1, _, u_id2, token2, _, _, ch_id = test_environment

    # The owner invites the user to new channel
    assert channel_invite(token2, ch_id, u_id1) == {}

    # The owner invites themself to new channel
    assert channel_invite(token2, ch_id, u_id2) == {}

    # The owner re-invites the user who is already member
    assert channel_invite(token2, ch_id, u_id1) == {}

def test_channel_invite_user_cases(test_environment):

    # set up environment
    u_id1, token1, u_id2, _, u_id3, _, ch_id = test_environment

    # The user invites the owner to new channel
    assert channel_invite(token1, ch_id, u_id2) == {}

    # The user invites themself to new channel
    assert channel_invite(token1, ch_id, u_id1) == {}

    # The user invites a stranger to new channel
    assert channel_invite(token1, ch_id, u_id3) == {}

def test_channel_invite_stranger_cases(test_environment, get_new_user_4):

    # set up environment
    u_id1, _, u_id2, _, u_id3, token3, ch_id = test_environment
    u_id4, _ = get_new_user_4

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

def test_channel_invite_validity(test_environment):

    # set up environment
    u_id1, _, u_id2, token2, u_id3, _, ch_id = test_environment

    # invalid channel id i.e. channel does not exist
    with pytest.raises(InputError):
        channel_invite(token2, ch_id + 1, u_id1)

    # invalid user id i.e. user does not exist
    with pytest.raises(InputError):
        channel_invite(token2, ch_id, u_id1 + u_id2 + u_id3)
