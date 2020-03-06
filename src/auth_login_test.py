from error import InputError
import pytest
import auth
import re  # Regular Expression Module


@pytest.fixture(scope="module")
def get_new_user():  
    # dummy data
    email = "z1234567@unsw.edu.au"
    password = "qwetyu"
    name_first = "Zhihan"
    name_last = "Qin"

    return email, password, name_first, name_last


# check if the email form is correct or not
# def check_email_form(email):
#     regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
#     # pass the regualar expression
#     # and the string in search() method
#     if (re.search(regex, email)):
#         return True
#     else:
#         return False


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
def test_login_invalid_email_form():
    # register a user
    email, password, name_first, name_last = get_new_user
    register_retval = auth.auth_register(email, password, name_first,
                                         name_last)
    u_id, token = register_retval['u_id'], register_retval['token']

    email.replace('@', '.')  # string is now "z1234567.unsw.edu.au"

    with pytest.raises(InputError):
        auth.auth_login(invalid_email, password)


# logging in from valid but nonregistered email
def test_non_registered_email():
    email, password, name_first, name_last = get_new_user

    with pytest.raises(InputError):
        auth.auth_login(email, password)


# incorrect password
def test_wrong_password(get_new_user):
    # register a user
    email, password, name_first, name_last = get_new_user
    register_retval = auth.auth_register(email, password, name_first,
                                         name_last)
    u_id, token = register_retval['u_id'], register_retval['token']

    # log user we just created out
    auth.auth_logout(token)

    incorrect_password = password + password  # double the password
    with pytest.raises(InputError):
        auth.auth_login(email, incorrect_password)
