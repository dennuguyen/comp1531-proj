import data
import pytest
import message
import channel
import channels
import error
import other
import sys
sys.path.append('../')

# Test user removing own message


def test_message_remove_message_user(get_new_user_1, get_new_user_2, get_channel_name_1):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Register test user 2
    _, token2 = get_new_user_2

    # Create test channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name,
                                     is_public=True)['channel_id']
    channel.channel_join(token=token2, channel_id=ch_id)  # user2 joins as member

    # User sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token=token2, channel_id=ch_id, message=msg_send)['message_id']

    # Actual test
    message.message_remove(token=token2, message_id=msg_id)

    # Search for the message
    retval = other.search(token=token1, query_str=msg_send)['messages']
    assert len(retval) == 0

    retval2 = channel.channel_messages(token=token1, channel_id=ch_id, start=0)['messages']
    assert len(retval2) == 0

    data.get_data().reset()

# Test owner removing user message
def test_message_remove_message_owner(get_new_user_1, get_new_user_2, get_channel_name_1):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Register test user 2
    _, token2 = get_new_user_2

    # Create test channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name,
                                     is_public=True)['channel_id']
    channel.channel_join(token=token2, channel_id=ch_id)  # user2 joins as member

    # User sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token=token2, channel_id=ch_id, message=msg_send)['message_id']

    # Actual test
    message.message_remove(token=token1, message_id=msg_id)

    # Search for the message
    retval = other.search(token=token1, query_str=msg_send)['messages']
    assert len(retval) == 0

    retval2 = channel.channel_messages(token=token1, channel_id=ch_id, start=0)['messages']
    assert len(retval2) == 0

    data.get_data().reset()   

# Slackr owner and channel owner can remove messages
def test_message_remove_message_owner_more(get_new_user_1, get_new_user_2, get_new_user_3, get_channel_name_1):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Register test user 2
    _, token2 = get_new_user_2

    # Register test user 3
    _, token3 = get_new_user_3

    # User 2 creates a channel where user 1 (slackr owner) automatically joins
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token2, name=ch_name,
                                     is_public=True)['channel_id']

    # User 3 joins as member
    channel.channel_join(token=token3, channel_id=ch_id)

    # User 2 sends message
    msg_send1 = 'The quick brown fox jumps over the lazy dog.'
    msg_id1 = message.message_send(token=token2, channel_id=ch_id, message=msg_send1)['message_id']

    # User 3 sends message
    msg_send2 = 'The quick brown fox jumps over the lazy dog.'
    msg_id2 = message.message_send(token=token3, channel_id=ch_id, message=msg_send2)['message_id']

    # Actual test
    message.message_remove(token=token1, message_id=msg_id1)
    message.message_remove(token=token1, message_id=msg_id2)

    # Search for the message
    retval = other.search(token=token1, query_str=msg_send1)['messages']
    assert len(retval) == 0

    retval = other.search(token=token1, query_str=msg_send2)['messages']
    assert len(retval) == 0

    # Check channel messages
    retval2 = channel.channel_messages(token=token1, channel_id=ch_id, start=0)['messages']
    assert len(retval2) == 0

    data.get_data().reset()

# Test InputError case
def test_message_remove_input_error(get_new_user_1, get_new_user_2):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Register test user 2
    _, token2 = get_new_user_2

    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    channel.channel_join(token=token2, channel_id=ch_id)  # user2 joins as member

    # User sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token=token2, channel_id=ch_id, message=msg_send)['message_id']

    # Testing message removal in empty channel
    message.message_remove(token=token1, message_id=msg_id)
    with pytest.raises(error.InputError):
        message.message_remove(token=token1, message_id=msg_id)

    data.get_data().reset()

# Test AccessError case
def test_message_remove_access_error(get_new_user_1, get_new_user_2):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Register test user 2
    _, token2 = get_new_user_2

    # Create test channel
    ch_id = channels.channels_create(token=token1, name='test_channel1',
                                     is_public=True)['channel_id']
    channel.channel_join(token=token2, channel_id=ch_id)  # user2 joins as member

    # Owner sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token=token1, channel_id=ch_id, message=msg_send)['message_id']

    # User tries to remove owner's message
    with pytest.raises(error.AccessError):
        message.message_remove(token=token2, message_id=msg_id)

    data.get_data().reset()