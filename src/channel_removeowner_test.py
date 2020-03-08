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


# test case where an owner removes another owner
def test_channel_removeowner_1():

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

    # user 2 joins channel and promoted to owner
    channel.channel_join(token2, ch_id)
    channel.channel_addowner(token1, ch_id, u_id2)

    # owner 1 removes owner 2
    assert channel.channel_removeowner(token1, ch_id, u_id2) == {}
    assert channel.channel_details(token2, ch_id) == {
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


# test case where owner removes themself
def test_channel_removeowner_2():

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

    # user 2 joins channel and promoted to owner
    channel.channel_join(token2, ch_id)
    channel.channel_addowner(token1, ch_id, u_id2)

    #Actual test
    assert channel.channel_removeowner(token1, ch_id, u_id1) == {}
    assert channel.channel_details(token1, ch_id) == {
        'name':
        'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'The',
                'name_last': 'Owner',
            },
        ],
        'all_members': [{
            'u_id': u_id1,
            'name_first': 'The',
            'name_last': 'Owner',
        }, {
            'u_id': u_id2,
            'name_first': 'The',
            'name_last': 'User',
        }]
    }


# test case where sole owner tries to remove themself
def test_channel_removeowner_3():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    u_id1, token1 = auth.auth_register(email1, password1, name_first1,
                                       name_last1)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # there cannot be no owners of the channel
    with pytest.raises(error.InputError):
        channel.channel_removeowner(token1, ch_id, u_id1)


# test case where member tries to remove owner
def test_channel_removeowner_4():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    u_id1, token1 = auth.auth_register(email1, password1, name_first1,
                                       name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    _, token2 = auth.auth_register(email2, password2, name_first2, name_last2)

    # user 1 creates a channel and user 2 joins the channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)
    channel.channel_join(token2, ch_id)

    with pytest.raises(error.AccessError):
        channel.channel_removeowner(token2, ch_id, u_id1)


# test case where owner tries to remove member
def test_channel_removeowner_invalid_user():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    u_id2, token2 = auth.auth_register(email2, password2, name_first2,
                                       name_last2)

    # user 1 creates a channel and user 2 joins the channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)
    channel.channel_join(token2, ch_id)

    # owner strips nonowner of owner permissions
    with pytest.raises(error.InputError):
        channel.channel_removeowner(token1, ch_id, u_id2)


# test case where invalid channel id is used
def test_channel_removeowner_invalid_channel_id():

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

    # user 2 joins channel and promoted to owner
    channel.channel_join(token2, ch_id)
    channel.channel_addowner(token1, ch_id, u_id2)

    # attempt to remove owner user 2 with invalid channel id
    with pytest.raises(error.InputError):
        channel.channel_removeowner(token1, ch_id + 1, u_id2)
