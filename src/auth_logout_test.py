import pytest
import auth
import error


# Test case valid token
def test_auth_logout(get_new_user_1):

    # Register a user
    _, token = get_new_user_1

    # Log out user
    assert auth.auth_logout(token)['is_success'] == True

    # Log out again with invalid token
    assert auth.auth_logout(token)['is_success'] == False


# Test case for invalid token
def test_auth_logout_invalid_token(get_new_user_1):

    # Register a user
    _, token = get_new_user_1

    # Log out user with invalid token
    assert auth.auth_logout(token + 'a')['is_success'] == False
