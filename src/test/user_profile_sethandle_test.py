import pytest
import user
import error
import sys
import data
sys.path.append('../')


# Base test case for setting new handle
def test_user_profile_sethandle(get_new_user_1, get_new_user_detail_1):

    # Register test user 1
    u_id, token = get_new_user_1
    email, _, name_first, name_last = get_new_user_detail_1

    # Actual test
    new_handle = (name_last + name_first).lower()
    user.user_profile_sethandle(token=token,handle_str=new_handle)
    assert user.user_profile(token=token,u_id=u_id) == {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': new_handle,
        },
    }
    # Clean the data
    data.get_data().reset()


# Test case for setting an invalid handle
def test_user_profile_sethandle_handle_invalid(get_new_user_1):

    # Register test user 1
    _, token = get_new_user_1

    # Actual test
    # Handle cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token=token,handle_str='')

    # Handle must be greater than 2 char
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token=token,handle_str='aa')

    # Handle must be less than 21 char
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token=token,handle_str= 'jamesbondthegreatofau')

    # Clean the data
    data.get_data().reset()


# Test case for handle that is already used
def test_user_profile_sethandle_handle_already_used(get_new_user_1,
                                                    get_new_user_detail_1,
                                                    get_new_user_2):

    # Register test user 1
    _, _ = get_new_user_1
    _, _, name_first, name_last = get_new_user_detail_1

    # Register test user 2
    _, token2 = get_new_user_2

    # user 2 sets handle to the same as user 1
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token=token2,handle_str= (name_first + name_last).lower())

    # Clean the data
    data.get_data().reset()