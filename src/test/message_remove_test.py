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
    ch_id = channels.channels_create(token1, ch_name,
                                     True)['channel_id']
    channel.channel_join(token2, ch_id)  # user2 joins as member

    # User sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token2, ch_id, msg_send)

    # Actual test
    message.message_remove(token2, msg_id)

    # Search for the message
    retval = other.search(token1, msg_send)['messages']
    assert len(retval) == 0

    retval2 = channel.channel_messages(token1, ch_id, 0)['messages']
    assert len(retval2) == 0


# Test owner removing user message
def test_message_remove_message_owner(get_new_user_1, get_new_user_2, get_channel_name_1):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Register test user 2
    _, token2 = get_new_user_2

    # Create test channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token1, ch_name,
                                     True)['channel_id']
    channel.channel_join(token2, ch_id)  # user2 joins as member

    # User sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token2, ch_id, msg_send)

    # Actual test
    message.message_remove(token1, msg_id)

    # Search for the message
    retval = other.search(token1, msg_send)['messages']
    assert len(retval) == 0

    retval2 = channel.channel_messages(token1, ch_id, 0)['messages']
    assert len(retval2) == 0


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
    ch_id = channels.channels_create(token2, ch_name,
                                     True)['channel_id']

    # User 3 joins as member
    channel.channel_join(token3, ch_id)

    # User 2 sends message
    msg_send1 = 'The quick brown fox jumps over the lazy dog.'
    msg_id1 = message.message_send(token2, ch_id, msg_send1)

    # User 3 sends message
    msg_send2 = 'The quick brown fox jumps over the lazy dog.'
    msg_id2 = message.message_send(token3, ch_id, msg_send2)

    # Actual test
    message.message_remove(token1, msg_id1)
    message.message_remove(token1, msg_id2)

    # Search for the message
    retval = other.search(token1, msg_send1)['messages']
    assert len(retval) == 0

    retval = other.search(token1, msg_send2)['messages']
    assert len(retval) == 0

    # Check channel messages
    retval2 = channel.channel_messages(token1, ch_id, 0)['messages']
    assert len(retval2) == 0


# Test InputError case
def test_message_remove_input_error(get_new_user_1, get_new_user_2):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Register test user 2
    _, token2 = get_new_user_2

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']
    channel.channel_join(token2, ch_id)  # user2 joins as member

    # User sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token2, ch_id, msg_send)

    # Testing message removal in empty channel
    message.message_remove(token1, msg_id)
    with pytest.raises(error.InputError):
        message.message_remove(token1, msg_id)


# Test AccessError case
def test_message_remove_access_error(get_new_user_1, get_new_user_2):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Register test user 2
    _, token2 = get_new_user_2

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']
    channel.channel_join(token2, ch_id)  # user2 joins as member

    # Owner sends message
    msg_send = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token1, ch_id, msg_send)

    # User tries to remove owner's message
    with pytest.raises(error.AccessError):
        message.message_remove(token2, msg_id)
