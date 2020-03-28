import pytest
import user
import error
import sys
import data
sys.path.append('../')


# basic test case for setting own name
def test_user_profile_setname(get_new_user_1, get_new_user_detail_1):

    # Register test user 1
    u_id, token = get_new_user_1
    email, _, name_first, name_last = get_new_user_detail_1

    # Actual test
    new_name_first = 'Test'
    new_name_last = 'User'
    user.user_profile_setname(token=token,name_first= new_name_first,name_last= new_name_last)
    assert user.user_profile(token=token,u_id= u_id) == {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': new_name_first,
            'name_last': new_name_last,
            'handle_str': (name_first + name_last).lower(),
        },
    }
    # Clean the data
    data.get_data().reset()


# test case for invalid name setting
def test_user_profile_setname_invalid(get_new_user_1, get_new_user_detail_1):

    # Register test user 1
    _, token = get_new_user_1
    _, _, name_first, name_last = get_new_user_detail_1

    # first name cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_setname(token=token,name_first= '',name_last= name_last)

    # last name cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_setname(token=token,name_first= name_first,name_last= '')

    # first name and last name cannot be empty

    with pytest.raises(error.InputError):
        user.user_profile_setname(token=token,name_first= '',name_last= '')

    # first name cannot be more than 50 char
    with pytest.raises(error.InputError):
        user.user_profile_setname(token=token,name_first= 'T' * 51,name_last= name_last)

    # last name cannot be more than 50 char
    with pytest.raises(error.InputError):
        user.user_profile_setname(token=token,name_first= name_first,name_last= 'B' * 51)

    # first name and last name cannot be more than 50 char
    with pytest.raises(error.InputError):
        user.user_profile_setname(token=token,name_first= 'T' * 51,name_last= 'B' * 51)

    # Clean the data
    data.get_data().reset()
