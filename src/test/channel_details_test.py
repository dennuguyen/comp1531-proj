import pytest
import channel
import error
import channels
import sys
sys.path.append('../')


# basic test for channel details
def test_channel_details(get_new_user_1, get_new_user_detail_1, get_new_user_2,
                         get_new_user_detail_2, get_channel_name_1):

    # get user 1
    u_id1, token1 = get_new_user_1
    _, _, name_first1, name_last1 = get_new_user_detail_1

    # get user 2
    u_id2, token2 = get_new_user_2
    _, _, name_first2, name_last2 = get_new_user_detail_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # user 2 joins channel
    channel.channel_join(token=token2, channel_id=ch_id)

    # check channel details
    assert channel.channel_details(token=token2, channel_id=ch_id) == {
        'name':
        ch_name,
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': name_first1,
                'name_last': name_last1,
            },
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': name_first1,
                'name_last': name_last1,
            },
            {
                'u_id': u_id2,
                'name_first': name_first2,
                'name_last': name_last2,
            },
        ],
    }


# nonmember of channel tries to call its details
def test_channel_details_invalid_user(get_new_user_1, get_new_user_2,
                                      get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    _, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # call detail() as non-authorised user 2 (stranger)
    with pytest.raises(error.AccessError):
        channel.channel_details(token=token2, channel_id=ch_id)

    # non-existent user's token
    with pytest.raises(error.AccessError):
        channel.channel_details(token=token1 + token2, channel_id=ch_id)


# invalid channel id
def test_channel_details_invalid_channel_id(get_new_user_1, get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # invalid channel id
    with pytest.raises(error.InputError):
        channel.channel_details(token=token1, channel_id=ch_id + 1000000)
