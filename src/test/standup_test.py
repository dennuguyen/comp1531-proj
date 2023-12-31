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


def test_standup_general(get_new_user_1, get_new_user_detail_1, get_new_user_2, get_new_user_detail_2, get_new_user_3, get_new_user_detail_3, get_channel_name_1):
    u_id, token1 = get_new_user_1
    _, token2 = get_new_user_2    
    _, token3 = get_new_user_3

    _, _, name1, _ = get_new_user_detail_1
    _, _, name2, _ = get_new_user_detail_2
    _, _, name3, _ = get_new_user_detail_3

    length = 3.0
    ch_id = channels.channels_create(token=token1, name=get_channel_name_1, is_public=True)['channel_id']
    channel.channel_join(token=token2, channel_id=ch_id)
    channel.channel_join(token=token3, channel_id=ch_id)

    t1 = threading.Thread(target=start_standup, args=(token1, ch_id, length))
    t2 = threading.Thread(target=check_is_active, args=(token1, ch_id))
    t3 = threading.Thread(target=send_messages, args=(token1, token2, token3, ch_id))
    t4 = threading.Thread(target=check_is_not_active, args=(token1, ch_id))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    time.sleep(length+0.5)
    message = data.get_data().get_message_with_message_id(0).get_message_dict()
    assert_msg = f'{name1}: test1\n{name2}: test2\n{name3}: test3\n'
    assert message['u_id'] == u_id
    assert message['message'] == assert_msg

    
    
def check_is_active(token, channel_id):
    time.sleep(1.0)
    assert standup.standup_active(token=token, channel_id=channel_id)['is_active'] == True

def check_is_not_active(token, channel_id):
    time.sleep(3.5)
    assert standup.standup_active(token=token, channel_id=channel_id)['is_active'] == False
    assert data.get_data().get_channel_with_ch_id(channel_id).get_standup_queue() == []

def start_standup(token, channel_id, length):
    standup.standup_start(token=token, channel_id=channel_id, length=length)

def send_messages(token1, token2, token3, channel_id):
    time.sleep(2.0)
    standup.standup_send(token=token1, channel_id=channel_id, message='test1')
    standup.standup_send(token=token2, channel_id=channel_id, message='test2')
    standup.standup_send(token=token3, channel_id=channel_id, message='test3')

    