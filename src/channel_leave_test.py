import pytest
from channel import channel_leave
from error import *
from channels import channels_create
from auth import auth_register

def test_environment():
    u_id1, token1 = auth_register('example@unsw.com', 'password', 'The', 'User')
    u_id2, token2 = auth_register('owner@unsw.com', 'password', 'The', 'Owner')
    u_id3, token3 = auth_register('stranger@unsw.com', 'password', 'A', 'Stranger')
    ch_id = channels_create(token2, 'New Channel', True) # u_id2 is owner

    return u_id1, token1, u_id2, token2, u_id3, token3, ch_id

# case where user leaves
def test_channel_leave_1():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()
    channel_invite(token2, ch_id, u_id1) # owner invites u_id1

    # user leaves
    assert channel_leave(token1, ch_id) == {}

# case where channel is owner leaves and user is promoted for channel populated by two
def test_channel_leave_2():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()
    channel_invite(token2, ch_id, u_id1) # owner invites u_id1

    # owner leaves
    assert channel_leave(token2, ch_id) == {}

# case where channel is populated by a sole owner
def test_channel_leave_3():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()

    # owner cannot leave
    with pytest.raises(InputError):
        channel_leave(token2, ch_id)

# invalid id and token cases
def test_channel_leave_validity():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()
    channel_invite(token2, ch_id, u_id1) # owner invites u_id1

    # invalid channel id
    with pytest.raises(InputError)
        channel_leave(token1, ch_id + 1)

    # invalid token
    with pytest.raises(InputError)
        channel_leave(token3, ch_id) # equivalent to stranger leaving channel
