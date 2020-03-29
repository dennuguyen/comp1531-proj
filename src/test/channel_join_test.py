import data
import pytest
import channel
import error
import channels
import sys
sys.path.append('../')

# stranger joins a public channel


def test_channel_join_public(get_new_user_1, get_new_user_detail_1, get_new_user_2,
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

    # user 2 (stranger) joins public channel

    print(data.get_data().get_channel_with_ch_id(ch_id).get_channel_dict())
    assert channel.channel_join(token=token2, channel_id=ch_id) == {}
    print(data.get_data().get_channel_with_ch_id(ch_id).get_channel_dict())
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

    data.get_data().reset()

# stranger joins a private channel
def test_channel_join_private(get_new_user_1, get_new_user_2, get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    _, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=False)['channel_id']

    # stranger joins private channel
    with pytest.raises(error.AccessError):
        channel.channel_join(token=token2, channel_id=ch_id)

    data.get_data().reset()


# invalid channel id
def test_channel_join_invalid_channel(get_new_user_1, get_new_user_2, get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    _, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=False)['channel_id']

    # stranger joins private channel
    with pytest.raises(error.InputError):
        channel.channel_join(token=token2, channel_id=(ch_id + 1000000))

    data.get_data().reset()

# rejoining a channel will raise InputError
def test_channel_join_rejoin(get_new_user_1, get_new_user_2, get_channel_name_1,
                             get_channel_name_2):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    _, token2 = get_new_user_2

    # user 1 creates a public channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # user 2 joins the channel
    channel.channel_join(token=token2, channel_id=ch_id)

    # user 2 joins the channel again
    with pytest.raises(error.InputError):
        channel.channel_join(token=token2, channel_id=ch_id)

    data.get_data().reset()