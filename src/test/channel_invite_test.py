import pytest
import channel
import error
import channels
import sys
import data
sys.path.append('../')

# inviting users to a public channel


def test_channel_invite_public(get_new_user_1, get_new_user_detail_1,
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
    u_id3, _ = get_new_user_3
    _, _, name_first3, name_last3 = get_new_user_detail_3

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # user 1 (owner) invites user 2 & 3
    assert channel.channel_invite(token=token1, channel_id=ch_id, u_id=u_id2) == {}
    assert channel.channel_invite(token=token1, channel_id=ch_id, u_id=u_id3) == {}

    # user 2 is immediately added to the channel
    assert channels.channels_list(token=token2) == {
        'channels': [
            {
                'channel_id': ch_id,
                'name': ch_name,
            },
        ],
    }
    

    # check channel details
    assert channel.channel_details(token=token1, channel_id=ch_id) == {
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

# inviting users to a private channel
def test_channel_invite_private(get_new_user_1, get_new_user_detail_1,
                                get_new_user_2, get_new_user_detail_2,
                                get_channel_name_1):

    # get user 1
    u_id1, token1 = get_new_user_1
    _, _, name_first1, name_last1 = get_new_user_detail_1

    # get user 2
    u_id2, token2 = get_new_user_2
    _, _, name_first2, name_last2 = get_new_user_detail_2

    # user 1 creates a private channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=False)['channel_id']

    # user 1 (owner) invites user 2
    assert channel.channel_invite(token=token1, channel_id=ch_id, u_id=u_id2) == {}

    # user 2 is immediately added to the channel
    assert channels.channels_list(token=token2) == {
        'channels': [
            {
                'channel_id': ch_id,
                'name': ch_name,
            },
        ],
    }

    # check channel details
    assert channel.channel_details(token=token1, channel_id=ch_id) == {
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

# self invitation has same test environment as re-invitating a member
def test_channel_self_invitation(get_new_user_1, get_new_user_detail_1,
                                 get_channel_name_1):
    
    # get user 1
    u_id1, token1 = get_new_user_1
    _, _, name_first1, name_last1 = get_new_user_detail_1

    # user 1 creates a private channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=False)['channel_id']

    # user 1 invites user 1 to the channel
    with pytest.raises(error.InputError):
        channel.channel_invite(token=token1, channel_id=ch_id, u_id=u_id1)

    data.get_data().reset()    

# test for access error cases
def test_channel_invite_access_error(get_new_user_1, get_new_user_detail_1,
                                     get_new_user_2, get_new_user_detail_2,
                                     get_new_user_3, get_new_user_detail_3,
                                     get_new_user_4, get_new_user_detail_4,
                                     get_channel_name_1):
    
    # get user 1
    u_id1, token1 = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2

    # get user 3
    u_id3, token3 = get_new_user_3

    # get user 4
    u_id4, _ = get_new_user_4

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # user 2 joins the channel as a member
    channel.channel_join(token=token2, channel_id=ch_id)

    # stranger invites the owner to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token=token3, channel_id=ch_id, u_id=u_id1)

    # stranger invites the user to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token=token3, channel_id=ch_id, u_id=u_id2)

    # stranger invites themself to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token=token3, channel_id=ch_id, u_id=u_id3)

    # stranger invites another stranger to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token=token3, channel_id=ch_id, u_id=u_id4)

    data.get_data().reset()    

# test case for invalid channel id
def test_channel_invite_invalid_channel(get_new_user_1, get_new_user_detail_1,
                                        get_new_user_2, get_new_user_detail_2,
                                        get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    u_id2, _ = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # invalid channel id (inviter is not a member of)
    with pytest.raises(error.InputError):
        channel.channel_invite(token=token1, channel_id=(ch_id + 1000000), u_id=u_id2)

    data.get_data().reset()    

# test case for invalid user id
def test_channel_invite_invalid_user(get_new_user_1, get_new_user_detail_1,
                                     get_new_user_2, get_new_user_detail_2,
                                     get_new_user_3, get_new_user_detail_3,
                                     get_new_user_4, get_new_user_detail_4,
                                     get_channel_name_1):

    # get user 1
    u_id1, token1 = get_new_user_1

    # get user 2
    u_id2, _ = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token=token1, name=ch_name, is_public=True)['channel_id']

    # invalid user id i.e. user does not exist
    with pytest.raises(error.InputError):
        channel.channel_invite(token=token1, channel_id=ch_id, u_id=(u_id2+1000000))

    data.get_data().reset()    