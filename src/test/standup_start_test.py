'''
TODO: test file for standup_active.py
'''
import pytest
import message
import channel
import channels
import error
import time
import threading
import other
import data
import sys
import standup
sys.path.append('../')

def test_standup(get_new_user_1, get_new_user_detail_1, get_new_user_2, get_new_user_detail_2, get_new_user_3, get_new_user_detail_3, get_channel_name_1):
    u_id, token1 = get_new_user_1
    _, token2 = get_new_user_2    
    _, token3 = get_new_user_3

    _, _, name1, _ = get_new_user_detail_1
    _, _, name2, _ = get_new_user_detail_2
    _, _, name3, _ = get_new_user_detail_3

    length = 5.0
    send_delay = 1.0
    ch_id = channels.channels_create(token=token1, name=get_channel_name_1, is_public=True)['channel_id']
    channel.channel_join(token=token2, channel_id=ch_id)
    channel.channel_join(token=token3, channel_id=ch_id)

    message1 = 'test1'
    message2 = 'test2'
    message3 = 'test3'


    t1 = threading.Timer(send_delay, standup.standup_send(token=token1, channel_id=ch_id, message=message1))
    t2 = threading.Timer(send_delay, standup.standup_send(token=token2, channel_id=ch_id, message=message2))
    t3 = threading.Timer(send_delay, standup.standup_send(token=token3, channel_id=ch_id, message=message3))

    standup.standup_start(token=token1, channel_id=ch_id, length=length)
    
    time.sleep(length+1.0)
    message = data.get_data().get_message_with_message_id(0)
    assert_msg = f'{name1}: {message1}\n{name2}: {message2}\n{name3}: {message3}\n'

    assert message.get_message_dict()['u_id'] == u_id
    assert message.get_message_dict()['message'] == assert_msg
    
def check_is_active(*, token, channel_id):
    assert standup.standup_active(token=token, channel_id=channel_id)['is_active'] == True
    pass
