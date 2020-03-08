import pytest
import user
import error

# User checks out own profile
def test_user_profile(get_new_user_1, get_new_user_detail_1):

    # Register test user 1
    u_id, token = get_new_user_1
    email, password, name_first, name_last = get_new_user_detail_1

    # Actual test
    assert user.user_profile(token, u_id) == {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': (name_first + name_last).lower,
        },
    }


# User checks out profile of invalid u_id
def test_user_profile_invalid_uid(get_new_user_1):

    # Register test user 1
    u_id, token = get_new_user_1

    # Actual test
    with pytest.raises(error.InputError):
        user.user_profile(token, (u_id + 1))
