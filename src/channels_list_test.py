import pytest
import error
import channels
import channel


# Test case for some public and private channels
def test_channels_list(get_new_user_1, get_new_user_2, get_channel_name_1, get_channel_name_2, get_channel_name_3, get_channel_name_4):

    # get user 1 and create channels
    token1 = get_new_user_1[1]
    ch_id1 = channels.channels_create(token1, get_channel_name_1, True)
    ch_id2 = channels.channels_create(token1, get_channel_name_2, False)
    _ = channels.channels_create(token1, get_channel_name_3, True)
    _ = channels.channels_create(token1, get_channel_name_4, False)

    # get user 2 and join some channels
    u_id2, token2 = get_new_user_2
    channel.channel_invite(token1, ch_id1, u_id2)
    channel.channel_invite(token1, ch_id2, u_id2)

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
        ],
    }

    # check channel list user 2 are members of
    assert channels.channels_list(token2) == test_list


# Test case for invalid token should raise AccessError
def test_channels_invalid_token(get_new_user_1):

    # get user 1
    token = get_new_user_1[1]

    # no given token
    with pytest.raises(error.AccessError):
        channels.channels_list('')

    # invalid token
    invalid_token = token + 'a'
    with pytest.raises(error.AccessError):
        channels.channels_list(invalid_token)


# Test case for empty channel list
def test_channels_list_empty(get_new_user_1, get_new_user_2, get_channel_name_1, get_channel_name_2, get_channel_name_3, get_channel_name_4):

    # get user 1 and create some channels
    token1 = get_new_user_1[1]
    _ = channels.channels_create(token1, get_channel_name_1, True)
    _ = channels.channels_create(token1, get_channel_name_2, False)
    _ = channels.channels_create(token1, get_channel_name_3, True)
    _ = channels.channels_create(token1, get_channel_name_4, False)

    # get user 2
    _, token2 = get_new_user_2

    # check channel list user 1 are members of
    assert channels.channels_list(token2) == {}
