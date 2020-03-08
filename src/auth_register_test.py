import auth
import pytest
import other
from error import InputError
import user

# Basic case
def test_auth_register(get_new_user_1, get_new_user_detail_1):
    email, password, name_first, name_last = get_new_user_detail_1
    u_id, token = get_new_user_1

    # Register and unpack u_id and token
    u_id, token = auth.auth_register(email, password, name_first, name_last)

    # Create user_dict
    user_dict = {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str':
            (name_first + name_last).lower(),  # makes string all lower case
        },
    }

    # Check if user exists after register
    assert user.user_profile(token, u_id) == user_dict
    assert user_dict in other.users_all(token)['users']


# Check email validity
def test_auth_register_invalid_email(get_new_user_detail_1):
    email, password, name_first, name_last = get_new_user_detail_1

    email.replace('@', '.')  # string is now "z1234567.unsw.edu.au"

    with pytest.raises(InputError):
        auth.auth_register(email, password, name_first, name_last)


# Email address cannot be registered twice
def test_auth_register_repeated_email(get_new_user_1, get_new_user_detail_1, get_new_user_detail_2):
    email, password, name_first, name_last = get_new_user_detail_1
    u_id, token = get_new_user_1

    email2, password2, name_first2, name_last2 = get_new_user_detail_2

    # Try registering again
    with pytest.raises(InputError):
        auth.auth_register(email, password2, name_first2, name_last2)


# Test case for password less than 6 char
def test_auth_register_invalid_password(get_new_user_1, get_new_user_detail_1):
    email, password, name_first, name_last = get_new_user_detail_1
    u_id, token = get_new_user_1

    invalid_password = password[:5]

    # Password less than 6 char raises InputError
    with pytest.raises(InputError):
        auth.auth_register(email, invalid_password, name_first, name_last)


# Ensure that name_first and name_last are both between 1 and 50 characters in length
def test_auth_register_invalid_name(get_new_user_detail_1):
    email, password, name_first, name_last = get_new_user_detail_1


    invalid_name_long = 'T'*51
    invalid_name_empty = ''

    # Test invalid first name only
    with pytest.raises(InputError):
        auth.auth_register(email, password, invalid_name_long, name_last)

    with pytest.raises(InputError):
        auth.auth_register(email, password, invalid_name_empty, name_last)

    # Test invalid last name only
    with pytest.raises(InputError):
        auth.auth_register(email, password, name_first, invalid_name_long)

    with pytest.raises(InputError):
        auth.auth_register(email, password, name_first, invalid_name_empty)

    # Test invalid first name and last name

    with pytest.raises(InputError):
        auth.auth_register(email, password, name_long, invalid_name_empty)

    with pytest.raises(InputError):
        auth.auth_register(email, password, name_empty, invalid_name_long)

    with pytest.raises(InputError):
        auth.auth_register(email, password, name_long, invalid_name_long)

    with pytest.raises(InputError):
        auth.auth_register(email, password, name_empty, invalid_name_empty)        

    
