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


def get_new_user_3():
    email = 'ted_bundy@unsw.edu.au'
    password = 'password'
    name_first = 'Ted'
    name_last = 'Bundy'
    return email, password, name_first, name_last


def get_new_user_4():
    email = 'randy@unsw.edu.au'
    password = 'password'
    name_first = 'Randy'
    name_last = 'Marshall'
    return email, password, name_first, name_last


def get_channel_name():
    ch_name = 'New Channel'
    return ch_name


# user 1 (owner) invites a stranger to a public channel
def test_channel_invite_public():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    u_id1, token1 = auth.auth_register(email1, password1, name_first1,
                                       name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, token2 = auth.auth_register(email2, password2, name_first2,
                                       name_last2)

    # get user 3
    email3, password3, name_first3, name_last3 = get_new_user_3()
    u_id3, _ = auth.auth_register(email3, password3, name_first3, name_last3)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # user 1 (owner) invites user 2 & 3
    assert channel.channel_invite(token1, ch_id, u_id2) == {}
    assert channel.channel_invite(token1, ch_id, u_id3) == {}

    # user 2 is immediately added to the channel
    assert channels.channels_list(token2) == {
        'channels': [
            {
                'channel_id': ch_id,
                'name': ch_name,
            },
        ],
    }

    # check channel details
    assert channel.channel_details(token1, ch_id) == {
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


# user 1 (owner) invites a stranger to a private channel
def test_channel_invite_private():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, token2 = auth.auth_register(email2, password2, name_first2,
                                       name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, False)

    # user 1 (owner) invites user 2
    assert channel.channel_invite(token1, ch_id, u_id2) == {}

    # user 2 is immediately added to the channel
    assert channels.channels_list(token2) == {
        'channels': [
            {
                'channel_id': ch_id,
                'name': ch_name,
            },
        ],
    }


# member of channel inviting a member of the same channel does nothing
def test_channel_member_self_invitation():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    u_id1, token1 = auth.auth_register(email1, password1, name_first1,
                                       name_last1)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # user 1 invites user 1 to the channel
    assert channel.channel_invite(token1, ch_id, u_id1) == {}

    # check for duplicates
    assert channels.channels_list(token1) == {
        'channels': [
            {
                'channel_id': ch_id,
                'name': ch_name,
            },
        ],
    }

    assert channel.channel_details(token1, ch_id) == {
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
        ],
    }


# test for access error cases
def test_channel_invite_access_error():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    u_id1, token1 = auth.auth_register(email1, password1, name_first1,
                                       name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, _ = auth.auth_register(email2, password2, name_first2, name_last2)

    # get user 3
    email3, password3, name_first3, name_last3 = get_new_user_3()
    u_id3, token3 = auth.auth_register(email3, password3, name_first3,
                                       name_last3)

    # get user 4
    email4, password4, name_first4, name_last4 = get_new_user_4()
    u_id4, _ = auth.auth_register(email4, password4, name_first4, name_last4)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # stranger invites the owner to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token3, ch_id, u_id1)

    # stranger invites the user to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token3, ch_id, u_id2)

    # stranger invites themself to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token3, ch_id, u_id3)

    # stranger invites another stranger to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token3, ch_id, u_id4)


# test case for invalid channel id
def test_channel_invite_invalid_channel():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, _ = auth.auth_register(email2, password2, name_first2, name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # invalid channel id (inviter is not a member of)
    with pytest.raises(error.InputError):
        channel.channel_invite(token1, ch_id + 1, u_id2)


# test case for invalid user id
def test_channel_invite_invalid_user():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    u_id1, token1 = auth.auth_register(email1, password1, name_first1,
                                       name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, _ = auth.auth_register(email2, password2, name_first2, name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # invalid user id i.e. user does not exist
    with pytest.raises(error.InputError):
        channel.channel_invite(token1, ch_id, u_id1 + u_id2)
