from error import InputError
import pytest
import auth
import re  # Regular Expression Module

def test_login(get_new_user):
    # register a user
    email, password, name_first, name_last = get_new_user
    register_retval = auth.auth_register(email, password, name_first,
                                         name_last)
    u_id, token = register_retval['u_id'], register_retval['token']

    # log user we just created out
    auth.auth_logout(token)

    login_retval = auth.auth_login(email, password)
    test_u_id = login_retval['u_id']

    assert u_id == test_u_id


# multiple logins are allowed
def test_login_already_logged_in(get_new_user):
    # register a user
    email, password, name_first, name_last = get_new_user
    register_retval = auth.auth_register(email, password, name_first,
                                         name_last)
    u_id1, token1 = register_retval['u_id'], register_retval['token']

    # logging in while logged in
    login_retval = auth.auth_login(email, password)
    u_id2, token2 = login_retval['u_id'], login_retval['token']

    assert u_id1 == u_id2  # user ids should be the same for each login
    assert token1 != token2  # tokens should be different for each login


# invalid email form during login
def test_login_invalid_email_form(get_new_user):
    # register a user
    email, password, name_first, name_last = get_new_user
    register_retval = auth.auth_register(email, password, name_first,
                                         name_last)
    token = register_retval['token']

    auth.auth_logout(token)

    email.replace('@', '.')  # string is now "z1234567.unsw.edu.au"

    with pytest.raises(InputError):
        auth.auth_login(email, password)


# logging in from valid but nonregistered email
def test_non_registered_email(get_new_user):
    email, password, _, _ = get_new_user

    with pytest.raises(InputError):
        auth.auth_login(email, password)


# incorrect password
def test_wrong_password(get_new_user):
    # register a user
    email, password, name_first, name_last = get_new_user
    register_retval = auth.auth_register(email, password, name_first,
                                         name_last)
    token =  register_retval['token']

    # log user we just created out
    auth.auth_logout(token)

    incorrect_password = password + password  # double the password
    with pytest.raises(InputError):
        auth.auth_login(email, incorrect_password)
