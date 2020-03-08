import pytest
import user
import user_test_helper
import error
import auth


# base test case for setting new handle
def test_user_profile_sethandle():

    # Register test user 1
    email, password, name_first, name_last = user_test_helper.get_new_user1()
    reg_retval = auth.auth_register(email, password, name_first, name_last)
    u_id, token = reg_retval['u_id'], reg_retval['token']

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


# test case for setting an invalid handle
def test_user_profile_sethandle_handle_invalid():

    # Register test user 1
    email, password, name_first, name_last = user_test_helper.get_new_user1()
    reg_retval = auth.auth_register(email, password, name_first, name_last)
    u_id, token = reg_retval['u_id'], reg_retval['token']

    # handle cannot be empty
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token, '')

    # handle must be greater than 2 char
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token, 'aa')

    # handle must be less than 21 char
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token, 'jamesbondthegreatofau')


# test case for handle that is already used
def test_user_profile_sethandle_handle_already_used():

    # Register test user 1
    email1, password1, name_first1, name_last1 = user_test_helper.get_new_user1(
    )
    reg_retval1 = auth.auth_register(email1, password1, name_first1,
                                     name_last1)
    u_id1, token1 = reg_retval1['u_id'], reg_retval1['token']

    # Register test user 2
    email2, password2, name_first2, name_last2 = user_test_helper.get_new_user2(
    )
    reg_retval2 = auth.auth_register(email2, password2, name_first2,
                                     name_last2)
    u_id2, token2 = reg_retval2['u_id'], reg_retval2['token']

    # user 2 sets handle to the same as user 1
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token2, (name_first1 + name_last1).lower())
