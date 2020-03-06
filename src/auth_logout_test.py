import pytest
import auth
from error import AccessError


# test case valid token
def test_logout(get_new_user):
    # register a user
    email, password, name_first, name_last = get_new_user
    register_retval = auth.auth_register(email, password, name_first,
                                         name_last)
    token = register_retval['token']

    # log out user
    assert auth.auth_logout(token)['is_success'] == True


# test case for invalid token
def test_logout_invalid_token(get_new_user):
    # register a user
    email, password, name_first, name_last = get_new_user
    register_retval = auth.auth_register(email, password, name_first,
                                         name_last)
    token =  register_retval['token']

    # log out user   
    with pytest.raises(AccessError):
        assert auth.auth_logout(token + 'a')['is_success'] == False
