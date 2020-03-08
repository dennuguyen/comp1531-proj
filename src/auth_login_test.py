from error import InputError
import pytest
import auth
import re  # Regular Expression Module


def test_login(get_new_user_1, get_new_user_detail_1):

    # Register a user
    email1, password1, _, _ = get_new_user_detail_1
    u_id1, token1 = get_new_user_1

    # Log user we just created out
    auth.auth_logout(token1)

    login_retval = auth.auth_login(email1, password1)
    test_u_id = login_retval['u_id']

    assert u_id1 == test_u_id


# Multiple logins are allowed
def test_login_already_logged_in(get_new_user_1, get_new_user_detail_1):

    # Register a user
    email1, password1, _, _ = get_new_user_detail_1
    u_id1, token1 = get_new_user_1

    # Logging in while logged in
    login_retval = auth.auth_login(email1, password1)
    u_id2, token2 = login_retval['u_id'], login_retval['token']

    assert u_id1 == u_id2  # User ids should be the same for each login
    assert token1 != token2  # Tokens should be different for each login


# Invalid email form during login
def test_login_invalid_email_form(get_new_user_1, get_new_user_detail_1):

    # Register a user
    email1, password1, _, _ = get_new_user_detail_1
    _, token1 = get_new_user_1

    auth.auth_logout(token1)

    email1.replace('@', '.')  # String is now "z1234567.unsw.edu.au"

    with pytest.raises(InputError):
        auth.auth_login(email1, password1)


# Logging in from valid but nonregistered email
def test_non_registered_email(get_new_user_detail_1):

    email1, password1, _, _ = get_new_user_detail_1

    with pytest.raises(InputError):
        auth.auth_login(email1, password1)


# Incorrect password
def test_wrong_password(get_new_user_1, get_new_user_detail_1):

    # Register a user
    email1, password1, _, _ = get_new_user_detail_1
    _, token1 = get_new_user_1

    # Log user we just created out
    auth.auth_logout(token1)

    incorrect_password = password1 + password1  # Double the password
    with pytest.raises(InputError):
        auth.auth_login(email1, incorrect_password)
