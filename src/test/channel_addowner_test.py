import pytest
import channel
import error
import channels
import sys
sys.path.append('../')


# test case where owner promotes a member to owner
def test_channel_addowner_promote_member(get_new_user_1, get_new_user_detail_1,
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

    # user 2 joins channel
    channel.channel_join(token=token2, channel_id=ch_id)

    # owner adds an owner
    assert channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id2) == {}

    # user 2 joins channel
    channel.channel_join(token=token2, channel_id=ch_id)

    # user 1 gives user 2 owner permissions
    assert channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id2) == {}
    assert channel.channel_details(token=token1, channel_id=ch_id) == {
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


# test case where owner promotes owner to owner
def test_channel_addowner_promote_owner(get_new_user_1, get_new_user_2,
                                        get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, channel_id=ch_name, is_public=True)['channel_id']

    # user 2 joins channel
    channel.channel_join(token=token2, channel_id=ch_id)

    # user 1 gives user 2 owner permissions
    assert channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id2) == {}

    # user 1 gives user 2 owner permissions again
    with pytest.raises(error.InputError):
        channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id2)


# test case where owner promotes stranger to owner
def test_channel_addowner_promote_stranger(get_new_user_1, get_new_user_2,
                                           get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    u_id2, _ = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, channel_id=ch_name, is_public=True)['channel_id']

    # owner promotes a stranger
    with pytest.raises(error.InputError):
        channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id2)


# test case where member promotes member to owner
def test_channel_addowner_unauthorised_member(get_new_user_1, get_new_user_2,
                                              get_new_user_3,
                                              get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2

    # get user 3
    u_id2, token3 = get_new_user_3

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, channel_id=ch_name, is_public=True)['channel_id']

    # user 2 and 3 joins channel
    channel.channel_join(token=token2, channel_id=ch_id)
    channel.channel_join(token=token3, channel_id=ch_id)

    # user 2 promotes user 2 (self)
    with pytest.raises(error.AccessError):
        channel.channel_addowner(token=token2, channel_id=ch_id, u_id=u_id2)

    # user 3 promotes user 2 (another member)
    with pytest.raises(error.AccessError):
        channel.channel_addowner(token=token3, channel_id=ch_id, u_id=u_id2)


# test case where stranger promotes member to owner
def test_channel_addowner_unauthorised_stranger(get_new_user_1, get_new_user_2,
                                                get_new_user_3,
                                                get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2

    # get user 3
    u_id2, token3 = get_new_user_3

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, channel_id=ch_name, is_public=True)['channel_id']

    # user 2 joins channel
    channel.channel_join(token=token2, channel_id=ch_id)

    # stranger promotes member
    with pytest.raises(error.AccessError):
        channel.channel_addowner(token=token3, channel_id=ch_id, u_id=u_id2)


# channel id validity
def test_channel_addowner_invalid_channel_id(get_new_user_1, get_new_user_2,
                                             get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, channel_id=ch_name, is_public=True)['channel_id']

    # user 2 joins channel
    channel.channel_join(token=token2, channel_id=ch_id)

    # invalid user id
    with pytest.raises(error.InputError):
        channel.channel_addowner(token=token1, channel_id=ch_id + 1, u_id=u_id2)


# u_id does not match any existing user
def test_channel_addowner_invalid_u_id(get_new_user_1, get_new_user_2,
                                       get_channel_name_1):

    # get user 1
    u_id1, token1 = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, channel_id=ch_name, is_public=True)['channel_id']

    # user 2 joins channel
    channel.channel_join(token=token2, channel_id=ch_id)

    # invalid user id
    with pytest.raises(error.InputError):
        channel.channel_addowner(token=token1, channel_id=ch_id, u_id=u_id1 + u_id2)
