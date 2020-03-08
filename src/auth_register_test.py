# if testing the register function, cannot call fixture functions with register

import auth
import pytest
import other
import error
import user


# Basic case
def test_auth_register(get_new_user_1, get_new_user_detail_1):
    email, password, name_first, name_last = get_new_user_detail_1
    u_id, token = get_new_user_1

    # Register and unpack u_id and token
    u_id, token = auth.auth_register(email, password, name_first, name_last)

    # Confirm the first registered user is the slackr owner
    assert u_id == 1

    # Create user_dict
    user_dict = {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str':
            (name_first + name_last).lower(),  # makes string all lower case
        },
    }

    # Check if user exists after register
    assert user.user_profile(token, u_id) == user_dict
    assert user_dict in other.users_all(token)['users']


# Check email validity
def test_auth_register_invalid_email(get_new_user_detail_1):
    email, password, name_first, name_last = get_new_user_detail_1

    email.replace('@', '.')  # string is now "z1234567.unsw.edu.au"

    with pytest.raises(error.InputError):
        auth.auth_register(email, password, name_first, name_last)


# Email address cannot be registered twice
def test_auth_register_repeated_email(get_new_user_1, get_new_user_detail_1, get_new_user_detail_2):
    email, _, _, _ = get_new_user_detail_1
    _, _ = get_new_user_1

    _, password2, name_first2, name_last2 = get_new_user_detail_2

    # Try registering again
    with pytest.raises(error.InputError):
        auth.auth_register(email, password2, name_first2, name_last2)


# Test case for password less than 6 char
def test_auth_register_invalid_password(get_new_user_1, get_new_user_detail_1):
    email, password, name_first, name_last = get_new_user_detail_1
    _, _ = get_new_user_1

    invalid_password = password[:5]

    # Password less than 6 char raises InputError
    with pytest.raises(error.InputError):
        auth.auth_register(email, invalid_password, name_first, name_last)


# Ensure that name_first and name_last are both between 1 and 50 characters in length
def test_auth_register_invalid_name(get_new_user_detail_1, get_invalid_user_name):
    email, password, name_first, name_last = get_new_user_detail_1

    invalid_name_long, invalid_name_empty = get_invalid_user_name

    # Test invalid first name only
    with pytest.raises(error.InputError):
        auth.auth_register(email, password, invalid_name_long, name_last)

    with pytest.raises(error.InputError):
        auth.auth_register(email, password, invalid_name_empty, name_last)

    # Test invalid last name only
    with pytest.raises(error.InputError):
        auth.auth_register(email, password, name_first, invalid_name_long)

    with pytest.raises(error.InputError):
        auth.auth_register(email, password, name_first, invalid_name_empty)

    # Test invalid first name and last name
    with pytest.raises(error.InputError):
        auth.auth_register(
            email, password, invalid_name_long, invalid_name_empty)

    with pytest.raises(error.InputError):
        auth.auth_register(
            email, password, invalid_name_empty, invalid_name_long)

    with pytest.raises(error.InputError):
        auth.auth_register(
            email, password, invalid_name_long, invalid_name_long)

    with pytest.raises(error.InputError):
        auth.auth_register(
            email, password, invalid_name_empty, invalid_name_empty)


# test for correct handle generation
def test_auth_register_handle(get_new_user_detail_1, get_new_user_detail_2, get_new_user_detail_3):

    # register user 1
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    _, token1 = auth.auth_register(
        email1, password1, name_first1, name_last1)

    # check for correct handle for user 1
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token1, (name_first1 + name_last1).lower())

    # register user 2 for same name as user 1
    email2, password2, _, _ = get_new_user_detail_2
    _, token2 = auth.auth_register(email2, password2, name_first1, name_first1)

    # cannot set handle as user 1's
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token2, (name_first1 + name_last1).lower())

    # check for correct handle for user 2
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(
            token2, (name_first1 + name_last1).lower() + '1')

    # register user 3
    email3, password3, _, _ = get_new_user_detail_3
    _, token3 = auth.auth_register(
        email3, password3, name_first1, name_last1)

    # check for correct handle for user 3
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(
            token3, (name_first1 + name_last1).lower() + '2')
