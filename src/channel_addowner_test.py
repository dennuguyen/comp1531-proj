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


def get_channel_name():
    ch_name = 'New Channel'
    return ch_name


# test case where owner promotes a member to owner
def test_channel_addowner_promote_member():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    u_id1, token1 = auth.auth_register(email1, password1, name_first1,
                                       name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, token2 = auth.auth_register(email2, password2, name_first2,
                                       name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # user 2 joins channel
    channel.channel_join(token2, ch_id)

    # user 1 gives user 2 owner permissions
    assert channel.channel_addowner(token1, ch_id, u_id2) == {}
    assert channel.channel_details(token1, ch_id) == {
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
def test_channel_addowner_promote_owner():

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

    # user 1 gives user 2 owner permissions
    assert channel.channel_addowner(token1, ch_id, u_id2) == {}

    # user 1 gives user 2 owner permissions again
    with pytest.raises(error.InputError):
        channel.channel_addowner(token1, ch_id, u_id2)


# test case where owner promotes stranger to owner
def test_channel_addowner_promote_stranger():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, _ = auth.auth_register(email2, password2, name_first2, name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # owner promotes a stranger
    with pytest.raises(error.AccessError):
        channel.channel_addowner(token1, ch_id, u_id2)


# test case where member promotes member to owner
def test_channel_addowner_unauthorised_member():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, token2 = auth.auth_register(email2, password2, name_first2,
                                       name_last2)

    # get user 3
    email3, password3, name_first3, name_last3 = get_new_user_3()
    _, token3 = auth.auth_register(email3, password3, name_first3, name_last3)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # user 2 and 3 joins channel
    channel.channel_join(token2, ch_id)
    channel.channel_join(token3, ch_id)

    # user 2 promotes user 2
    with pytest.raises(error.AccessError):
        channel.channel_addowner(token2, ch_id, u_id2)

    # user 3 promotes user 2
    with pytest.raises(error.AccessError):
        channel.channel_addowner(token3, ch_id, u_id2)


# test case where stranger promotes member to owner
def test_channel_addowner_unauthorised_stranger():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, token2 = auth.auth_register(email2, password2, name_first2,
                                       name_last2)

    # get user 3
    email3, password3, name_first3, name_last3 = get_new_user_3()
    _, token3 = auth.auth_register(email3, password3, name_first3, name_last3)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # user 2 joins channel
    channel.channel_join(token2, ch_id)

    # stranger promotes member
    with pytest.raises(error.AccessError):
        channel.channel_addowner(token3, ch_id, u_id2)


# validity cases
def test_channel_addowner_invalid_channel_id():

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

    # invalid user id
    with pytest.raises(error.InputError):
        channel.channel_addowner(token1, ch_id + 1, u_id2)


def test_channel_addowner_invalid_u_id():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    u_id1, token1 = auth.auth_register(email1, password1, name_first1,
                                       name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, token2 = auth.auth_register(email2, password2, name_first2,
                                       name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # user 2 joins channel
    channel.channel_join(token2, ch_id)

    # invalid user id
    with pytest.raises(error.InputError):
        channel.channel_addowner(token1, ch_id, u_id1 + u_id2)
