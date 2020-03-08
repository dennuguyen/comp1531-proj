import pytest
import auth
from error import AccessError


# Test case valid token
def test_logout(get_new_user_1):
    # Register a user
    u_id, token = get_new_user_1

    # Log out user
    assert auth.auth_logout(token)['is_success'] == True


# Test case for invalid token
def test_logout_invalid_token(get_new_user_1):
    # Register a user
    u_id, token = get_new_user_1

    # Log out user   
    assert auth.auth_logout(token + 'a')['is_success'] == False
