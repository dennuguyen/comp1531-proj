import pytest
import message
import auth
import channel
import channels
import error
import other
import datetime


# User edits their own message
def test_message_edit(get_new_user_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Send message 1
    msg_send1 = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token1, ch_id, msg_send1)

    # Edit message
    msg_send2 = 'The quick brown dog jumps over the lazy fox.'
    time_before = datetime.datetime.now()
    message.message_edit(token1, msg_id, msg_send2)
    time_after = datetime.datetime.now()

    # Check the first message
    retval1 = other.search(token1, msg_send1)['messages']
    assert len(retval1) == 0

    # Check the edited message
    retval2 = other.search(token1, msg_send2)['messages']
    assert retval2[0]['message_id'] == msg_id
    assert retval2[0]['u_id'] == u_id1
    assert retval2[0]['message'] == msg_send2
    assert retval2[0]['time_created'] > time_before
    assert retval2[0]['time_created'] < time_after

    # Check for duplicate
    assert len(retval2) == 1


# User edits another user's message
def test_message_edit_by_non_authorised_user(get_new_user_1, get_new_user_2):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Register test user 2
    _, token2 = get_new_user_2

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']
    channel.channel_join(token2, ch_id)  # user2 joins as member

    # Send message 1
    msg_send1 = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token1, ch_id, msg_send1)

    # Edit message
    msg_send2 = 'The quick brown dog jumps over the lazy fox.'
    with pytest.raises(error.AccessError):
        message.message_edit(token2, msg_id, msg_send2)


# Channel owner can edit any message
def test_message_edit_by_owner(get_new_user_1, get_new_user_2):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1

    # Register test user 2
    _, token2 = get_new_user_2

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']
    channel.channel_join(token2, ch_id)  # user2 joins as member

    # Send message 1
    msg_send1 = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token2, ch_id, msg_send1)

    # Edit message
    msg_send2 = 'The quick brown dog jumps over the lazy fox.'
    time_before = datetime.datetime.now()
    message.message_edit(token1, msg_id, msg_send2)
    time_after = datetime.datetime.now()

    # Check the first message
    retval1 = other.search(token1, msg_send1)['messages']
    assert len(retval1) == 0

    # Check the message
    retval2 = other.search(token1, msg_send2)['messages']
    assert retval2[0]['message_id'] == msg_id
    assert retval2[0]['u_id'] == u_id1
    assert retval2[0]['message'] == msg_send2
    assert retval2[0]['time_created'] > time_before
    assert retval2[0]['time_created'] < time_after

    # Check for duplicate
    assert len(retval2) == 1

    retval3 = channel.channel_messages(token1, ch_id, 0)['messages']
    assert len(retval3) == 1    

    retval = other.search(token1, msg_send)['messages']
    assert len(retval) == 0

# Owner of slackr can edit any message
def test_message_edit_by_owner_of_slackr(get_new_user_1, get_new_user_2, get_new_user_3, get_channel_name_1):

    # Register test user 1 (owner)
    u_id1, token1 = get_new_user_1

    # Register test user 2
    u_id2, token2 = get_new_user_2

    # Register test user 3
    u_id3, token3 = get_new_user_3


    # Create test channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token2, ch_name,
                                     True)['channel_id']
    channel.channel_join(token3, ch_id)  # user3 joins as member

    # Send message 1
    msg_send = 'The quick brown fox jumps over the lazy dog1.'
    msg_id = message.message_send(token2, ch_id, msg_send)

    # Send message 2

    msg_send2 = 'The quick brown fox jumps over the lazy dog2.'
    msg_id2 = message.message_send(token3, ch_id, msg_send2)

    # Edit message 1
    msg_send3 = 'The quick brown dog jumps over the lazy fox.'
    time_before = datetime.datetime.now()
    message.message_edit(token1, msg_id, msg_send3)
    time_after = datetime.datetime.now()

    # Edit message 2
    msg_send4 = 'The quick brown dog jumps over the lazy fox.'
    time_before = datetime.datetime.now()
    message.message_edit(token1, msg_id2, msg_send4)
    time_after = datetime.datetime.now()    

    # Check the first message
    retval1 = other.search(token1, msg_send)['messages']
    assert len(retval1) == 0

    # Check the message
    retval2 = other.search(token1, msg_send3)['messages']
    assert retval2[0]['message_id'] == msg_id
    assert retval2[0]['u_id'] == u_id1
    assert retval2[0]['message'] == msg_send3
    assert retval2[0]['time_created'] > time_before
    assert retval2[0]['time_created'] < time_after

    # Check the second message
    retval1 = other.search(token1, msg_send2)['messages']
    assert len(retval1) == 0

    # Check the message
    retval2 = other.search(token1, msg_send4)['messages']
    assert retval2[1]['message_id'] == msg_id2
    assert retval2[1]['u_id'] == u_id1
    assert retval2[1]['message'] == msg_send4
    assert retval2[1]['time_created'] > time_before
    assert retval2[1]['time_created'] < time_after

    # Check for duplicate
    assert len(retval2) == 2

    retval3 = channel.channel_messages(token2, ch_id, 0)['messages']
    assert len(retval3) == 2    

    retval4 = other.search(token2, msg_send)['messages']
    assert len(retval4) == 0 

    retval5 = other.search(token3, msg_send2)['messages']
    assert len(retval5) == 0       

# Message edit is empty therefore must be removed
def test_message_edit_to_remove(get_new_user_1):

    # Register test user 1 (owner)
    _, token1 = get_new_user_1

    # Create test channel
    ch_id = channels.channels_create(token1, 'test_channel1',
                                     True)['channel_id']

    # Send message 1
    msg_send1 = 'The quick brown fox jumps over the lazy dog.'
    msg_id = message.message_send(token1, ch_id, msg_send1)

    # Edit message
    msg_send2 = ''
    message.message_edit(token1, msg_id, msg_send2)

    # Message does not exist
    retval1 = other.search(token1, msg_send1)['messages']
    assert len(retval1) == 0

    retval2 = other.search(token1, msg_send2)['messages']
    assert len(retval2) == 0

    retval3 = channel.channel_messages(token1, ch_id, 0)['messages']
    assert len(retval3) == 0
