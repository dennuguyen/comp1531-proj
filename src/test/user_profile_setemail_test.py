import pytest
import user
import error
import sys
import data
sys.path.append('../')

# user changes their own email


def test_user_profile_setemail(get_new_user_1, get_new_user_detail_1):


    print("\n\nLMAO TEST 1 #########\n\n")

    # Register test user 1
    u_id, token = get_new_user_1
    email, _, name_first, name_last = get_new_user_detail_1

    # Actual test
    new_email = 'prefix' + email
    user.user_profile_setemail(token=token,email=new_email)
    assert user.user_profile(token=token,u_id=u_id) == {
        'user': {
            'u_id': u_id,
            'email': new_email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': (name_first + name_last).lower(),
        },
    }
    # Clean the data
    data.get_data().reset()


# email address of incorrect format
def test_user_profile_setemail_invalid_email(get_new_user_1):

    print("\n\nLMAO TEST 2 #########\n\n")
    # Register test user 1
    _, token = get_new_user_1

    # Actual test
    with pytest.raises(error.InputError):
        user.user_profile_setemail(token=token,email='z1111111x.unsw.edu.au')

    with pytest.raises(error.InputError):
        user.user_profile_setemail(token=token,email='z1111111xunsweduau')

    # Clean the data
    data.get_data().reset()


# email address already used
def test_user_profile_setemail_email_already_used(get_new_user_1,
                                                  get_new_user_detail_1,
                                                  get_new_user_2):

    print("\n\nLMAO TEST 3 #########\n\n")
    # Register test user 1 and 2
    _, _ = get_new_user_1
    email, _, _, _ = get_new_user_detail_1
    _, token2 = get_new_user_2


    # Actual test
    with pytest.raises(error.InputError):
        user.user_profile_setemail(token=token2,email=email)

    # Clean the data
    data.get_data().reset()
