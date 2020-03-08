import pytest
import user
import user_test_helper
import error


# basic test case for setting own name
def test_user_profile_setname():

    # Register test user 1
    email, password, name_first, name_last = user_test_helper.get_new_user1()
    reg_retval = auth.auth_register(email, password, name_first, name_last)
    u_id, token = reg_retval['u_id'], reg_retval['token']

    # Actual test
    new_name_first = name_first + 'suffix'
    new_name_last = 'prefix' + name_last
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
def test_user_profile_setname_invalid():

    # Register test user 1
    email, password, name_first, name_last = user_test_helper.get_new_user1()
    reg_retval = auth.auth_register(email, password, name_first, name_last)
    u_id, token = reg_retval['u_id'], reg_retval['token']

    # first name cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, '', name_last)

    # last name cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, name_first, '')

    # first name cannot be more than 50 char
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, 'T' * 51, name_last)

    # last name cannot be more than 50 char
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, name_first, 'B' * 51)
