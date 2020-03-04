import pytest
from channel import channel_join, channel_addowner
from error import *
from channels import channels_create
from auth import auth_register

def test_environment():
    u_id1, token1 = auth_register('owner@unsw.com', 'password', 'The', 'Owner')
    u_id2, token2 = auth_register('stranger@unsw.com', 'password', 'A', 'Stranger')
    ch_id = channels_create(token1, 'New Channel', True)

    return u_id1, token1, u_id2, token2, ch_id

# test case where owner promotes a member to owner
def test_channel_addowner_1():

    # set up environment
    u_id1, token1, u_id2, token2, ch_id = test_environment()
    channel_join(token2, ch_id)

    # owner adds an owner
    assert channel_addowner(token1, ch_id, u_id2) == {}

# test case where owner promotes owner to owner
def test_channel_addowner_2():
    
    # set up environment
    u_id1, token1, u_id2, token2, ch_id = test_environment()

    # owner promotes someone
    with pytest.raises(InputError):
        channel_addowner(token1, ch_id, u_id1)

# test case where owner promotes stranger to owner
def test_channel_addowner_3():

    # set up environment
    u_id1, token1, u_id2, token2, ch_id = test_environment()

    # owner promotes a stranger
    with pytest.raises(AccessError):
        channel_addowner(token1, ch_id, u_id2)

# test case where member promotes member to owner
def test_channel_addowner_4():

    # set up environment
    u_id1, token1, u_id2, token2, ch_id = test_environment()
    channel_join(token2, ch_id)

    # owner promotes a stranger
    with pytest.raises(AccessError):
        channel_addowner(token2, ch_id, u_id2)

# test case where stranger promotes member to owner
def test_channel_addowner_5():

    # set up environment
    u_id1, token1, u_id2, token2, ch_id = test_environment()

    # stranger promotes someone
    with pytest.raises(AccessError):
        channel_addowner(token2, ch_id, u_id1)

# validity cases
def test_channel_addowner_6():

    # set up environment
    u_id1, token1, u_id2, token2, ch_id = test_environment()

    # invalid user id
    with pytest.raises(InputError):
        channel_addowner(token1, ch_id, u_id1 + u_id2)

    # invalid channel id
    with pytest.raises(InputError):
        channel_addowner(token1, ch_id + 1, u_id1)
