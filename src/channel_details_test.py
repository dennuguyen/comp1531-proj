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


# basic test for channel details
def test_channel_details():

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

    # check channel details
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


# nonmember of channel tries to call its details
def test_channel_details_invalid_user():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # get user 2
    email2, password2, name_first2, name_last2 = get_new_user_2()
    _, token2 = auth.auth_register(email2, password2, name_first2, name_last2)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # call detail() as non-authorised user
    with pytest.raises(error.AccessError):
        channel.channel_details(token2, ch_id)

    # non-existent user's token
    with pytest.raises():
        channel.channel_details(token1 + 'a', ch_id)


# invalid channel id
def test_channel_details_invalid_channel():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # invalid channel id
    with pytest.raises(error.InputError):
        channel.channel_details(token1, ch_id + 1)
