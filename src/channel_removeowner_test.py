import pytest
from channel import channel_join, channel_removeowner, channel_addowner
from error import *
from channels import channels_create
from auth import auth_register

def test_environment():
    u_id1, token1 = auth_register('example@unsw.com', 'password', 'The', 'User')
    u_id2, token2 = auth_register('owner@unsw.com', 'password', 'The', 'Owner')
    u_id3, token3 = auth_register('stranger@unsw.com', 'password', 'A', 'Stranger')
    ch_id = channels_create(token2, 'New Channel', True) # u_id2 is owner

    return u_id1, token1, u_id2, token2, u_id3, token3, ch_id

# test case where an owner removes another owner
def test_channel_removeowner_1():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()
    channel_join(token1, ch_id)
    channel_addowner(token2, ch_id, u_id1) # promote user 1 to owner

    # owner 2 removes owner 1
    assert channel_removeowner(token1, ch_id, u_id2) == {}


############### COMPLETE TEST FUNCTIONS BELOW #####################

# test case where owner tries to remove themself
def test_channel_removeowner_2():
    
    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()

# test case where sole owner tries to remove themself
def test_channel_removeowner_2():
    
    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()

# test case where member tries to remove owner
def test_channel_removeowner_2():
    
    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()
