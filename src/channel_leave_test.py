import pytest
import channel
import error
import channels


# case where user leaves
def test_channel_leave_user_leaves(get_new_user_1, get_new_user_2, get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    _, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token1, ch_name, True)['channel_id']

    # user 2 joins channel
    channel.channel_join(token2, ch_id)

    # user 2 leaves
    assert channel.channel_leave(token2, ch_id) == {}

    # user 2 should not be member of any channels
    assert channels.channels_list(token2)['channels'] == []


# case where channel is populated by a sole owner
def test_channel_leave_sole_owner(get_new_user_1, get_new_user_2, get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    u_id2, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token1, ch_name, True)['channel_id']

    # user 2 joins channel
    channel.channel_join(token2, ch_id)

    # owner leaves
    with pytest.raises(error.InputError):
        channel.channel_leave(token1, ch_id)

    # give user 2 owner permissions
    channel.channel_addowner(token1, ch_id, u_id2)

    # user 1 (owner) can now leave
    assert channel.channel_leave(token1, ch_id) == {}
    assert channels.channels_list(token1)['channels'] == []


# invalid channel id
def test_channel_leave_invalid_channel_id(get_new_user_1, get_new_user_2, get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    _, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token1, ch_name, True)['channel_id']

    # user 2 joins channel
    channel.channel_join(token2, ch_id)

    # invalid channel id
    with pytest.raises(error.InputError):
        channel.channel_leave(token2, (ch_id + 1))


# stranger leaving channel or invalid token
def test_channel_leave_unauthorised_user(get_new_user_1, get_new_user_2, get_channel_name_1):

    # get user 1
    _, token1 = get_new_user_1

    # get user 2
    _, token2 = get_new_user_2

    # user 1 creates a channel
    ch_name = get_channel_name_1
    ch_id = channels.channels_create(token1, ch_name, True)['channel_id']

    # user 2 tries to leave the channel
    with pytest.raises(error.AccessError):
        channel.channel_leave(token2, ch_id)
