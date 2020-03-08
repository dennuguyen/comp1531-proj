import pytest
import channel
import error
import channels
import auth
import message


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


# base case for channel messages
def test_channel_messages():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # add some messages to the channel
    for integer in range(1, 6):
        message = 'test message ' + f'{integer}'
        message.message_send(token1, ch_id, message)
        integer += 1

    retval = channel.channel_messages(token1, ch_id, 0)
    for no_msg in retval['messages']:
        no_msg += 1

    assert no_msg == 5
    assert retval['start'] == 0
    assert retval['end'] == -1


def test_channel_messages_greater_than_50():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    # if messages length > 50
    for integer in range(1, 56):
        message = 'test message ' + f'{integer}'
        message.message_send(token1, ch_id, message)
        integer += 1

    retval = channel.channel_messages(token1, ch_id, 0)
    for no_msg in retval['messages']:
        no_msg += 1

    assert no_msg == 50
    assert retval['start'] == 0
    assert retval['end'] == 50


def test_channel_messages_invalid_channel_id():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    with pytest.raises(error.InputError):
        channel.channel_messages(token1, ch_id + 1, 0)


def test_channel_messages_start_is_greater():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    for integer in range(1, 6):
        message = 'test message ' + f'{integer}'
        message.message_send(token1, ch_id, message)
        integer += 1

    with pytest.raises(error.InputError):
        channel.channel_messages(token1, ch_id, 10)


def test_channel_messages_unauthorised_user():

    # get user 1
    email1, password1, name_first1, name_last1 = get_new_user_1()
    _, token1 = auth.auth_register(email1, password1, name_first1, name_last1)

    # user 1 creates a channel
    ch_name = get_channel_name()
    ch_id = channels.channels_create(token1, ch_name, True)

    with pytest.raises(error.AccessError):
        channel.channel_messages(token1, ch_id, 10)