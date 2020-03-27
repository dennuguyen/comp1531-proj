import pytest
import error
import auth
import data
import sys
sys.path.append('../')


def test_auth_login(get_new_user_detail_1):
    """
    Register a user
    Log them out
    Log them in again
    """
    data.get_data().reset()

    # Register a user
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    auth_retval1 = auth.auth_register(email=email1,
                                      password=password1,
                                      name_first=name_first1,
                                      name_last=name_last1)
    u_id1, token1 = auth_retval1['u_id'], auth_retval1['token']

    # Log out user
    auth.auth_logout(token=token1)

    # Log in user
    login_retval = auth.auth_login(email=email1, password=password1)
    u_id2, _ = login_retval['u_id'], login_retval['token']

    # Check user id are the same
    assert u_id1 == u_id2


def test_auth_login_already_logged_in(get_new_user_detail_1):
    """
    Register a user
    Log them in again
    """
    data.get_data().reset()

    # Register a user which logs them in
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    auth_retval1 = auth.auth_register(email=email1,
                                      password=password1,
                                      name_first=name_first1,
                                      name_last=name_last1)
    u_id1, token1 = auth_retval1['u_id'], auth_retval1['token']

    # Logging in while logged in
    login_retval = auth.auth_login(email=email1, password=password1)
    u_id2, token2 = login_retval['u_id'], login_retval['token']

    # User ids and tokens should be the same
    assert u_id1 == u_id2
    assert token1 != token2


# Invalid email form during login
def test_auth_login_invalid_email_form(get_new_user_detail_1):

    data.get_data().reset()

    # Register a user
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    auth.auth_register(email=email1,
                       password=password1,
                       name_first=name_first1,
                       name_last=name_last1)

    # Invalidate the email
    email1 = email1.replace('@', '.')  # String is now "z1234567.unsw.edu.au"

    # Log in user with invalid email
    with pytest.raises(error.InputError):
        auth.auth_login(email=email1, password=password1)


# Logging in from valid but nonregistered email
def test_auth_login_non_registered_email(get_new_user_detail_1):

    data.get_data().reset()

    # Get user details
    email1, password1, _, _ = get_new_user_detail_1

    # Log in a user without registering
    with pytest.raises(error.InputError):
        auth.auth_login(email=email1, password=password1)


# Incorrect password
def test_auth_login_wrong_password(get_new_user_detail_1):

    data.get_data().reset()

    # Register a user
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    auth.auth_register(email=email1,
                       password=password1,
                       name_first=name_first1,
                       name_last=name_last1)

    # Log in with incorrect password
    incorrect_password = password1 + password1  # Double the password
    with pytest.raises(error.InputError):
        auth.auth_login(email=email1, password=incorrect_password)
