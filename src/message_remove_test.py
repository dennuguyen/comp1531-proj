import pytest
import message
import auth
import channel
import channels
import error
import other


# Test user removing own message
def test_message_remove_message_user(get_new_user_1, get_new_user_2):

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

    # Actual test
    message.message_remove(token2, msg_id)

    # Search for the message
    retval = other.search(token1, msg_send)['messages']
    assert len(retval) == 0


# Test owner removing user message
def test_message_remove_message_owner(get_new_user_1, get_new_user_2):

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

    # Actual test
    message.message_remove(token1, msg_id)

    # Search for the message
    retval = other.search(token1, msg_send)['messages']
    assert len(retval) == 0


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
