import error
import pytest
import auth
import re  # Regular Expression Module


def test_auth_login(get_new_user_1, get_new_user_detail_1):

    # Register a user
    email1, password1, _, _ = get_new_user_detail_1
    u_id1, token1 = get_new_user_1

    # Log out user
    auth.auth_logout(token1)

    # Log in user
    login_retval = auth.auth_login(email1, password1)
    u_id2, _ = login_retval['u_id'], login_retval['token']

    # Check user id are the same
    assert u_id1 == u_id2


# Multiple logins are allowed
def test_auth_login_already_logged_in(get_new_user_1, get_new_user_detail_1):

    # Register a user
    email1, password1, _, _ = get_new_user_detail_1
    u_id1, _ = get_new_user_1

    # Logging in while logged in
    login_retval = auth.auth_login(email1, password1)
    u_id2, _ = login_retval['u_id'], login_retval['token']

    # User ids and tokens should be the same
    assert u_id1 == u_id2


# Invalid email form during login
def test_auth_login_invalid_email_form(get_new_user_1, get_new_user_detail_1):

    # Register a user
    email1, password1, _, _ = get_new_user_detail_1
    _, token1 = get_new_user_1

    # Log out user
    auth.auth_logout(token1)

    # Invalidate the email
    email1.replace('@', '.')  # String is now "z1234567.unsw.edu.au"

    # Log in user with invalid email
    with pytest.raises(error.InputError):
        auth.auth_login(email1, password1)


# Logging in from valid but nonregistered email
def test_auth_login_non_registered_email(get_new_user_detail_1):

    # Get user details
    email1, password1, _, _ = get_new_user_detail_1

    # Log in a user without registering
    with pytest.raises(error.InputError):
        auth.auth_login(email1, password1)


# Incorrect password
def test_auth_login_wrong_password(get_new_user_1, get_new_user_detail_1):

    # Register a user
    email1, password1, _, _ = get_new_user_detail_1
    _, token1 = get_new_user_1

    # Log out user
    auth.auth_logout(token1)

    # Log in with incorrect password
    incorrect_password = password1 + password1  # Double the password
    with pytest.raises(error.InputError):
        auth.auth_login(email1, incorrect_password)
