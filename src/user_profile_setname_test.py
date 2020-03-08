import pytest
import user
import user_test_helper
import error


# basic test case for setting own name
def test_user_profile_setname():

    # Register test user 1
    email, password, name_first, name_last = user_test_helper.get_new_user1()
    reg_retval = auth.auth_register(email, password, name_first, name_last)
    u_id, token = reg_retval['u_id'], reg_retval['token'])

    # Actual test
    user.user_profile_setname(token, 'Ted', 'Bundy')
    assert user.user_profile(token, u_id) == {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': 'Ted',
            'name_last': 'Bundy',
            'handle_str': 'tedbundy',
        },
    }


# test case for invalid name setting
def test_user_profile_setname_invalid():

    # Register test user 1
    email, password, name_first, name_last = user_test_helper.get_new_user1()
    reg_retval = auth.auth_register(email, password, name_first, name_last)
    u_id, token = reg_retval['u_id'], reg_retval['token'])

    # first name cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, '', 'Bundy')
    
    # last name cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, 'Ted', '')

    # first name cannot be more than 50 char
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, 'T' * 51, 'Bundy')
    
    # last name cannot be more than 50 char
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, 'Ted', 'B' * 51)
