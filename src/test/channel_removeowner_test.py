import data
import pytest
import channel
import channels
import error
import sys
sys.path.append('../')


# test case where slackr owner is removed
def test_channel_removeowner_slackr_owner(get_new_user_1, get_new_user_detail_1,
                                          get_new_user_2, get_new_user_detail_2,
                                          get_channel_name_1):

    # get user 1
    u_id1, token1 = get_new_user_1
    _, _, name_first1, name_last1 = get_new_user_detail_1

    # get user 2
    u_id2, token2 = get_new_user_2
    _, _, name_first2, name_last2 = get_new_user_detail_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # user 2 joins channel and promoted to owner
    channel.channel_join(token=token2, channel_id=ch_id)
    channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id2)

    # user 2 (channel owner) cannot remove user 1 (slackr owner)
    with pytest.raises(error.InputError):
        channel.channel_removeowner(token=token2, channel_id=ch_id, u_id=u_id1)

    # user 1 (slackr owner) cannot remove themself
    with pytest.raises(error.InputError):
        channel.channel_removeowner(token=token1, channel_id=ch_id, u_id=u_id1)

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
            {
                'u_id': u_id2,
                'name_first': name_first2,
                'name_last': name_last2,
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

# test case where channel owner is removed
def test_channel_removeowner_channel_owner(get_new_user_1, get_new_user_detail_1,
                                           get_new_user_2, get_new_user_detail_2,
                                           get_new_user_3, get_new_user_detail_3,
                                           get_channel_name_1):

    # get user 1
    u_id1, token1 = get_new_user_1
    _, _, name_first1, name_last1 = get_new_user_detail_1

    # get user 2
    u_id2, token2 = get_new_user_2
    _, _, name_first2, name_last2 = get_new_user_detail_2

    # get user 3
    u_id3, token3 = get_new_user_3
    _, _, name_first3, name_last3 = get_new_user_detail_3

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # user 2 joins channel and promoted to owner
    channel.channel_join(token=token2, channel_id=ch_id)
    channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id2)

    # user 3 joins channel and promoted to owner
    channel.channel_join(token=token3, channel_id=ch_id)
    channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id3)

    # user 2 (channel owner) removes user 3 (channel owner)
    assert channel.channel_removeowner(token=token2, channel_id=ch_id, u_id=u_id3) == {}

    # user 1 (slackr owner) removes user 2 (channel owner)
    assert channel.channel_removeowner(token=token1, channel_id=ch_id, u_id=u_id2) == {}

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
            {
                'u_id': u_id3,
                'name_first': name_first3,
                'name_last': name_last3,
            },
        ],
    }

    data.get_data().reset()

# test case where sole owner tries to remove themself
def test_channel_remove_themself(get_new_user_1, get_new_user_2,
                                        get_new_user_detail_2,
                                        get_channel_name_1):

    # get user 1
    _, _ = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2
    _, _, name_first2, name_last2 = get_new_user_detail_2

    # user 2 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token2, name=ch_name, is_public=True)['channel_id']

    # user 2 (channel owner) tries to remove themself
    with pytest.raises(error.InputError):
        channel.channel_removeowner(token=token2, channel_id=ch_id, u_id=u_id2)

    data.get_data().reset()

# test case where stranger and member tries to remove owner without owner permissions
def test_channel_removeowner_unauthorised_user(get_new_user_1, get_new_user_2,
                                               get_new_user_3, get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2

    # get user 3
    _, token3 = get_new_user_3

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # user 2 joins channel and promoted to owner
    channel.channel_join(token=token2, channel_id=ch_id)
    channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id2)

    # user 3 (stranger) tries to remove user 2 (owner)
    with pytest.raises(error.AccessError):
        channel.channel_removeowner(token=token3, channel_id=ch_id, u_id=u_id2)

    # user 3 joins channel and promoted to owner
    channel.channel_join(token=token3, channel_id=ch_id)

    # user 3 (member) tries to remove user 2 (owner)
    with pytest.raises(error.AccessError):
        channel.channel_removeowner(token=token3, channel_id=ch_id, u_id=u_id2)

    data.get_data().reset()

# test case where owner tries to remove member who is not an owner
def test_channel_removeowner_invalid_user(get_new_user_1, get_new_user_2,
                                          get_new_user_3, get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2

    # get user 3
    u_id3, _ = get_new_user_3

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # user 2 joins channel and promoted to owner
    channel.channel_join(token=token2, channel_id=ch_id)

    # user 1 (channel owner) removes user 2 (member)
    with pytest.raises(error.InputError):
        channel.channel_removeowner(token=token1, channel_id=ch_id, u_id=u_id2)

    # user 1 (slackr owner) removes user 3 (stranger)
    with pytest.raises(error.InputError):
        channel.channel_removeowner(token=token1, channel_id=ch_id, u_id=u_id3)

    data.get_data().reset()

# test case where owner has invalid channel id
def test_channel_removeowner_invalid_channel_id(get_new_user_1, get_new_user_detail_1,
                                                get_new_user_2, get_new_user_detail_2,
                                                get_new_user_3, get_new_user_detail_3,
                                                get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # user 2 joins channel and promoted to owner
    channel.channel_join(token=token2, channel_id=ch_id)
    channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id2)

    # attempt to remove owner user 2 with invalid channel id
    with pytest.raises(error.InputError):
        channel.channel_removeowner(token=token1, channel_id=ch_id + 1000000, u_id=u_id2)

    data.get_data().reset()