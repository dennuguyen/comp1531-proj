import pytest
import user
import user_test_helper
import error
import auth


# user changes their own email
def test_user_profile_setemail():

    # Register test user 1
    email, password, name_first, name_last = user_test_helper.get_new_user1()
    reg_retval = auth.auth_register(email, password, name_first, name_last)
    u_id, token = reg_retval['u_id'], reg_retval['token']

    # Actual test
    new_email = 'prefix' + email
    user.user_profile_setemail(token, new_email)
    assert user.user_profile(token, u_id) == {
        'user': {
            'u_id': u_id,
            'email': new_email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': (name_first + name_last).lower(),
        },
    }


# email address of incorrect format
def test_user_profile_setemail_invalid_email():

    # Register test user 1
    email, password, name_first, name_last = user_test_helper.get_new_user1()
    reg_retval = auth.auth_register(email, password, name_first, name_last)
    u_id, token = reg_retval['u_id'], reg_retval['token']

    # Actual test
    with pytest.raises(error.InputError):
        user.user_profile_setemail(token, 'z1111111x.unsw.edu.au')

    with pytest.raises(error.InputError):
        user.user_profile_setemail(token, 'z1111111xunsweduau')


# email address already used
def test_user_profile_setemail_email_already_used():

    # Register test user 1
    email1, password1, name_first1, name_last1 = user_test_helper.get_new_user1(
    )
    reg_retval1 = auth.auth_register(email1, password1, name_first1,
                                     name_last1)

    # Register test user 2
    email2, password2, name_first2, name_last2 = user_test_helper.get_new_user2(
    )
    reg_retval2 = auth.auth_register(email2, password2, name_first2,
                                     name_last2)
    u_id2, token2 = reg_retval2['u_id'], reg_retval2['token']

    # Actual test
    with pytest.raises(error.InputError):
        user.user_profile_setemail(token2, email1)
