import pytest
from channel import channel_join
from error import *
from channels import channels_create
from auth import auth_register

def test_environment():
    u_id1, token1 = auth_register('owner@unsw.com', 'password', 'The', 'Owner')
    u_id2, token2 = auth_register('stranger@unsw.com', 'password', 'A', 'Stranger')
    ch_id1 = channels_create(token1, 'Public Channel', True)
    ch_id2 = channels_create(token1, 'Private Channel', False)

    return u_id1, token1, u_id2, token2, ch_id1, ch_id2

def test_channel_join_1():

    # set up environment
    u_id1, token1, u_id2, token2, ch_id1, ch_id2 = test_environment()

    # stranger joins public channel
    assert channel_join(token2, ch_id1) == {}

    # stranger joins private channel
    with pytest.raises(AccessError):
        channel_join(token2, ch_id2)

def test_channel_join_2():

    # set up environment
    u_id1, token1, u_id2, token2, ch_id1, ch_id2 = test_environment()

    # owner tries to join public channel again
    assert channel_join(token1, ch_id1) == {}

    # owner tries to join private channel again
    assert channel_join(token1, ch_id2) == {}
