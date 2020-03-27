'''
TODO: test file for standup_active.py
'''
import pytest
import message
import channel
import channels
import error
import time
import other
from data import get_data
import sys
import standup
sys.path.append('../')

def test_standup_start(get_new_user_1, get_new_user_2, get_new_user_3, get_channel_name_1):
    _, token1 = get_new_user_1
    _, token2 = get_new_user_2    
    _, token3 = get_new_user_3

    ch_id = channels.channels_create(token=token1, name=get_channel_name_1, is_public=True)['channel_id']
    channel.channel_join(token=token2, channel_id=ch_id)
    channel.channel_join(token=token3, channel_id=ch_id)

    standup.standup_active(token=token1, channel_id=ch_id)
    
