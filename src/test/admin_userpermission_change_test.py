'''
Test file for admin.py
'''
import pytest
import error
import admin
from data import get_data
import sys
sys.path.append('../')

def test_admin_userpermission_change(get_new_user_1, get_new_user_2):
    
    # Register an admin
    u_id1, token1 = get_new_user_1

    # Register an user
    u_id2, token2 = get_new_user_2

    # Assertion
    assert get_data().get_user_with_token(token2).get_permission_id() == 2
    admin.admin_userpermission_change(token=token1, u_id=u_id2, permission_id=1)
    assert get_data().get_user_with_token(token2).get_permission_id() == 1

    get_data().reset()

def test_invalid_admin_change_permission(get_new_user_1, get_new_user_2, get_new_user_3):
    # Register an admin
    u_id1, token1 = get_new_user_1

    # Register an user2
    u_id2, token2 = get_new_user_2

    # Register an user3
    u_id3, token3 = get_new_user_3

    # Invalid admin change permission
    with pytest.raises(error.AccessError):
        admin.admin_userpermission_change(token=token2, u_id=u_id3, permission_id=1)
    
    get_data().reset()

def test_change_permission_invalid_user(get_new_user_1, get_new_user_2):
    
    # Register an admin
    u_id1, token1 = get_new_user_1

    # Register an user2
    u_id2, token2 = get_new_user_2

    # Admin change permission of an invalid user
    with pytest.raises(error.InputError):
        admin.admin_userpermission_change(token=token1, u_id=u_id2+1, permission_id=1)

    get_data().reset()

def test_invalid_permission_id_input(get_new_user_1, get_new_user_2):

    # Register an admin
    u_id1, token1 = get_new_user_1

    # Register an user2
    u_id2, token2 = get_new_user_2

    # Wrongly input permission id
    with pytest.raises(error.InputError):
        admin.admin_userpermission_change(token=token1, u_id=u_id2+1, permission_id=3)

    get_data().reset()
