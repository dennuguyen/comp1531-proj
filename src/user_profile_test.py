#Raymond: Tests for user_profile function

import pytest
import user
import user_test_helper
import error


# user checks out own profile
def test_user_profile():

    # Register test user 1
    email, password, name_first, name_last = user_test_helper.get_new_user1()
    reg_retval = auth.auth_register(email, password, name_first, name_last)
    u_id, token = reg_retval['u_id'], reg_retval['token'])

    # Actual test
    assert user.user_profile(token, u_id) == {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': (name_first + name_last).lower(),
        },
    }


# user checks out profile of invalid u_id
def test_user_profile_invalid_uid():

    # Register test user 1
    email, password, name_first, name_last = user_test_helper.get_new_user1()
    reg_retval = auth.auth_register(email, password, name_first, name_last)
    u_id, token = reg_retval['u_id'], reg_retval['token'])

    # Actual test
    with pytest.raises(error.InputError):
        user.user_profile(token, (u_id + 1))
