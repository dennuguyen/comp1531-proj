import pytest
import user
import error
import auth


# Base test case for setting new handle
def test_user_profile_sethandle(get_new_user_1, get_new_user_detail_1):

    # Register test user 1
    u_id, token = get_new_user_1
    email, password, name_first, name_last = get_new_user_detail_1

    # Actual test
    new_handle = (name_last + name_first).lower()
    user.user_profile_sethandle(token, new_handle)
    assert user.user_profile(token, u_id) == {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': new_handle,
        },
    }


# Test case for setting an invalid handle
def test_user_profile_sethandle_handle_invalid(get_new_user_1):

    # Register test user 1
    u_id, token = get_new_user_1
    
    # Actual test
    # Handle cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token, '')

    # Handle must be greater than 2 char
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token, 'aa')

    # Handle must be less than 21 char
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token, 'jamesbondthegreatofau')


# Test case for handle that is already used
def test_user_profile_sethandle_handle_already_used(get_new_user_1, get_new_user_detail_1, get_new_user_2):

    # Register test user 1
    u_id, token = get_new_user_1
    email, password, name_first, name_last = get_new_user_detail_1

    # Register test user 2
    u_id2, token2 = get_new_user_2


    # user 2 sets handle to the same as user 1
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token2, (name_first1 + name_last1).lower())
