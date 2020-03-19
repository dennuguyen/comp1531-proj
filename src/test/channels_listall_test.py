import pytest
import channel
import channels
import error
import sys
sys.path.append('../')

# Test case use of listall for public channels


def test_channels_listall_public(get_new_user_1, get_new_user_2, get_channel_name_1, get_channel_name_2, get_channel_name_3, get_channel_name_4):

    # get user 1 and create channels
    token1 = get_new_user_1[1]
    ch_id1 = channels.channels_create(token1, get_channel_name_1, True)
    ch_id2 = channels.channels_create(token1, get_channel_name_2, True)
    ch_id3 = channels.channels_create(token1, get_channel_name_3, True)
    ch_id4 = channels.channels_create(token1, get_channel_name_4, True)

    # get user 2 and join some channels
    u_id2, token2 = get_new_user_2
    channel.channel_invite(token1, ch_id1, u_id2)
    channel.channel_invite(token1, ch_id3, u_id2)

    # prepare test_list for comparison
    test_list = {
        'channels': [
            {
                'channel_id': ch_id1,
                'name': get_channel_name_1,
            },
            {
                'channel_id': ch_id2,
                'name': get_channel_name_2,
            },
            {
                'channel_id': ch_id3,
                'name': get_channel_name_3,
            },
            {
                'channel_id': ch_id4,
                'name': get_channel_name_4,
            },
        ],
    }

    # listall should return all public channels
    assert channels.channels_listall(token1) == channels.channels_listall(
        token2) == test_list


# Test case use of listall for private channels
def test_channels_listall_private(get_new_user_1, get_new_user_2, get_channel_name_1, get_channel_name_2, get_channel_name_3, get_channel_name_4):

    # get user 1 and create channels
    token1 = get_new_user_1[1]
    ch_id1 = channels.channels_create(token1, get_channel_name_1, False)
    ch_id2 = channels.channels_create(token1, get_channel_name_2, False)
    ch_id3 = channels.channels_create(token1, get_channel_name_3, False)
    ch_id4 = channels.channels_create(token1, get_channel_name_4, False)

    # get user 2 and join some channels
    u_id2, token2 = get_new_user_2
    channel.channel_invite(token1, ch_id1, u_id2)
    channel.channel_invite(token1, ch_id3, u_id2)

    # prepare test_list for comparison
    test_list = {
        'channels': [
            {
                'channel_id': ch_id1,
                'name': get_channel_name_1,
            },
            {
                'channel_id': ch_id2,
                'name': get_channel_name_2,
            },
            {
                'channel_id': ch_id3,
                'name': get_channel_name_3,
            },
            {
                'channel_id': ch_id4,
                'name': get_channel_name_4,
            },
        ],
    }

    # listall should return all private channels
    assert channels.channels_listall(token1) == channels.channels_listall(
        token2) == test_list


# Test case for invalid token should raise AccessError
def test_channels_invalid_token(get_new_user_1):

    token = get_new_user_1[1]

    # no given token
    with pytest.raises(error.AccessError):
        channels.channels_listall('')

    # invalid token
    invalid_token = token + 'a'
    with pytest.raises(error.AccessError):
        channels.channels_listall(invalid_token)


# Test case for empty channel list
def test_channels_list_empty(get_new_user_1):

    # get a user but do not create any channels
    token = get_new_user_1[1]

    # list all the channels
    assert channels.channels_listall(token) == {}
