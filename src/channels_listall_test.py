import pytest
import channel
import channels
import error


def test_channels_listall(get_new_user_1, get_new_user_2, get_channel_name_1, get_channel_name_2, get_channel_name_3, get_channel_name_4):

    token1 = get_new_user_1[1]
    ch_id1 = channels.channels_create(token1, get_channel_name_1, True)
    ch_id2 = channels.channels_create(token1, get_channel_name_2, True)
    ch_id3 = channels.channels_create(token1, get_channel_name_3, True)
    ch_id4 = channels.channels_create(token1, get_channel_name_4, True)

    token2 = get_new_user_2[1]

    channel.channel_join(token2, ch_id1)
    channel.channel_join(token2, ch_id3)

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

    # valid token
    assert channels.channels_listall(token1) == channels.channels_listall(
        token2) == test_list


def test_channels_invalid_token(get_new_user_1):

    token = get_new_user_1[1]

    # no given token
    assert channels.channels_listall('') == {}

    # invalid token
    invalid_token = token + 'a'
    assert channels.channels_listall(invalid_token) == {}


def test_channels_list_empty(get_new_user_1):

    token = get_new_user_1[1]
    assert channels.channels_listall(token) == {}
