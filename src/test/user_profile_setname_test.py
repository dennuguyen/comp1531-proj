import pytest
import user
import error
import sys
sys.path.append('../')


# basic test case for setting own name
def test_user_profile_setname(get_new_user_1, get_new_user_detail_1):

    # Register test user 1
    u_id, token = get_new_user_1
    email, _, _, _ = get_new_user_detail_1

    # Actual test
    new_name_first = 'Test'
    new_name_last = 'User'
    user.user_profile_setname(token, new_name_first, new_name_last)
    assert user.user_profile(token, u_id) == {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': new_name_first,
            'name_last': new_name_last,
            'handle_str': (new_name_first + new_name_last).lower(),
        },
    }


# test case for invalid name setting
def test_user_profile_setname_invalid(get_new_user_1, get_new_user_detail_1):

    # Register test user 1
    _, token = get_new_user_1
    _, _, name_first, name_last = get_new_user_detail_1

    # first name cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, '', name_last)

    # last name cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, name_first, '')

    # first name and last name cannot be empty

    with pytest.raises(error.InputError):
        user.user_profile_setname(token, '', '')

    # first name cannot be more than 50 char
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, 'T' * 51, name_last)

    # last name cannot be more than 50 char
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, name_first, 'B' * 51)

    # first name and last name cannot be more than 50 char
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, 'T' * 51, 'B' * 51)
