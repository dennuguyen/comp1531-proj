import pytest
import channel
import error
import channels
import auth


def get_new_user_1():
    email = 'john_doe@unsw.edu.au'
    password = 'password'
    name_first = 'John'
    name_last = 'Doe'
    return email, password, name_first, name_last


def get_new_user_2():
    email = 'hugh_jackman@unsw.edu.au'
    password = 'password'
    name_first = 'Hugh'
    name_last = 'Jackman'
    return email, password, name_first, name_last


def get_channel_name():
    ch_name = 'New Channel'
    return ch_name


# test case where user leaves
def test_channel_leave_user():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    _, token2 = auth.auth_register(email2, password2, name_first2, name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # user 2 joins channel
    channel.channel_join(token2, ch_id)

    # user 2 leaves
    assert channel.channel_leave(token2, ch_id) == {}

    # user 2 should not be member of any channels
    assert channels.channels_list(token2)['channels'] == []


# test case where channel is populated by a sole owner
def test_channel_leave_owner():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, token2 = auth.auth_register(email2, password2, name_first2,
                                       name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

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


# test case for invalid channel id
def test_channel_leave_invalid_channel_id():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    _, token2 = auth.auth_register(email2, password2, name_first2, name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # user 2 joins channel
    channel.channel_join(token2, ch_id)

    # invalid channel id
    with pytest.raises(error.InputError):
        channel.channel_leave(token2, ch_id + 1)


# test case for stranger leaving channel or invalid token
def test_channel_leave_unauthorised_user():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    _, token2 = auth.auth_register(email2, password2, name_first2, name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # invalid token
    with pytest.raises(error.AccessError):
        channel.channel_leave(token2, ch_id)
