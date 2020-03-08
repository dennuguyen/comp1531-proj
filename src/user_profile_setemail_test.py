import pytest
import user
import error
import auth


# user changes their own email
def test_user_profile_setemail(get_new_user_1, get_new_user_detail_1):

    # Register test user 1
    u_id, token = get_new_user_1
    email, password, name_first, name_last = get_new_user_detail_1

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
def test_user_profile_setemail_invalid_email(get_new_user_1):

    # Register test user 1
    u_id, token = get_new_user_1


    # Actual test
    with pytest.raises(error.InputError):
        user.user_profile_setemail(token, 'z1111111x.unsw.edu.au')

    with pytest.raises(error.InputError):
        user.user_profile_setemail(token, 'z1111111xunsweduau')


# email address already used
def test_user_profile_setemail_email_already_used(get_new_user_1, get_new_user_detail_1, get_new_user_2):

    # Register test user 1 and 2
    u_id, token = get_new_user_1
    email, password, name_first, name_last = get_new_user_detail_1
    u_id2, token2 = get_new_user_2


    # Actual test
    with pytest.raises(error.InputError):
        user.user_profile_setemail(token2, email)
