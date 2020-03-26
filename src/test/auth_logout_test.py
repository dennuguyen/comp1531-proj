import pytest
import auth
import sys
sys.path.append('../')
import data


# Test case valid token
def test_auth_logout(get_new_user_detail_1):

    data.get_data().reset()

    # Register a user
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    auth_retval1 = auth.auth_register(email=email1,
                                      password=password1,
                                      name_first=name_first1,
                                      name_last=name_last1)
    _, token1 = auth_retval1['u_id'], auth_retval1['token']

    # Log out user
    assert auth.auth_logout(token=token1)['is_success'] == True

    # Log out again with invalid token
    assert auth.auth_logout(token=token1)['is_success'] == False


# Test case for invalid token
def test_auth_logout_invalid_token(get_new_user_detail_1):

    data.get_data().reset()

    # Register a user
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    auth_retval1 = auth.auth_register(email=email1,
                                      password=password1,
                                      name_first=name_first1,
                                      name_last=name_last1)
    _, token1 = auth_retval1['u_id'], auth_retval1['token']

    # Log out user with invalid token
    assert auth.auth_logout(token=token1 + 'a')['is_success'] == False
