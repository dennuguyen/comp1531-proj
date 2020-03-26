import data
import pytest
import channel
import error
import channels
import message
import sys
sys.path.append('../')

# if message length <= 50
def test_channel_messages_less_than_50(get_new_user_1):

    # set up environment
    _, token1 = get_new_user_1
    ch_id = channels.channels_create(token=token1, name='New Channel', is_public=True)['channel_id']

    # create dummy messages
    for i in range(5):
        msg = 'test message ' + str(i + 1)
        message.message_send(token=token1, channel_id=ch_id, message=msg)
        i += 1

    retval = channel.channel_messages(token=token1, channel_id=ch_id, start=0)

    assert len(retval['messages']) == 5
    assert retval['start'] == 0
    assert retval['end'] == -1

    data.get_data().reset()

# if messages length > 50
def test_channel_messages_greater_than_50(get_new_user_1):

    # set up environment
    _, token1 = get_new_user_1
    ch_id = channels.channels_create(token=token1, name='New Channel', is_public=True)['channel_id']

    for i in range(124):
        msg = 'test message ' + str(i+1)
        message.message_send(token=token1, channel_id=ch_id, message=msg)
        i += 1

    retval = channel.channel_messages(token=token1, channel_id=ch_id, start=0)
    assert len(retval['messages']) == 50
    assert retval['start'] == 0
    assert retval['end'] == 50
    retval = channel.channel_messages(token=token1, channel_id=ch_id, start=50)
    assert len(retval['messages']) == 50
    assert retval['start'] == 50
    assert retval['end'] == 100
    retval = channel.channel_messages(token=token1, channel_id=ch_id, start=100)
    assert len(retval['messages']) == 24
    assert retval['start'] == 100
    assert retval['end'] == -1

    data.get_data().reset()

def test_channel_messages_invalid_channel_id(get_new_user_1):

    # set up environment
    _, token1 = get_new_user_1
    ch_id = channels.channels_create(token=token1, name='New Channel', is_public=True)['channel_id']

    with pytest.raises(error.InputError):
        channel.channel_messages(token=token1, channel_id=(ch_id + 1000000), start=0)

    data.get_data().reset()

def test_channel_messages_start_is_greater(get_new_user_1):

    _, token1 = get_new_user_1
    ch_id = channels.channels_create(token=token1, name='New Channel', is_public=True)

    for i in range(5):
        msg = 'test message ' + str(i + 1)
        message.message_send(token=token1, channel_id=ch_id, message=msg)
        i += 1

    with pytest.raises(error.InputError):
        channel.channel_messages(token=token1, channel_id=ch_id, start=10)

    data.get_data().reset()

def test_channel_messages_unauthorised_user(get_new_user_1, get_new_user_2):

    _, token1 = get_new_user_1
    _, token2 = get_new_user_2

    ch_id = channels.channels_create(token=token1, name='New Channel', is_public=True)['channel_id']

    with pytest.raises(error.AccessError):
        channel.channel_messages(token=token2, channel_id=ch_id, start=10)

    data.get_data().reset()