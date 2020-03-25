# if testing the register function, cannot call fixture functions with register
import sys
sys.path.append('../')
import auth
import pytest
import other
import error
import user


# Basic case
def test_auth_register(get_new_user_detail_1):

    # Register and unpack u_id and token
    email, password, name_first, name_last = get_new_user_detail_1
    u_id, token = auth.auth_register(email=email,
                                     password=password,
                                     name_first=name_first,
                                     name_last=name_last)

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
# def test_auth_register_invalid_email(get_new_user_detail_1):
#     email, password, name_first, name_last = get_new_user_detail_1

#     email.replace('@', '.')  # string is now "z1234567.unsw.edu.au"

#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email,
#                            password=password,
#                            name_first=name_first,
#                            name_last=name_last)

# # Email form must follow {64}@{255} chars
# def test_auth_login_long_email_form(get_new_user_detail_1):

#     # Get user 1
#     email1, password1, name_first1, name_last1 = get_new_user_detail_1

#     # local_part is 65 char and domain is 256 char
#     local_part1 = 'T' * 65
#     local_part2 = 'T' * 64
#     domain1 = 'D' * 255
#     domain2 = 'D' * 256

#     # Make some emails
#     email1 = local_part1 + '@' + domain1
#     email2 = local_part2 + '@' + domain2
#     email3 = local_part1 + '@' + domain2

#     # Tests
#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email1,
#                            password=password1,
#                            name_first=name_first1,
#                            name_last=name_last1)

#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email2,
#                            password=password1,
#                            name_first=name_first1,
#                            name_last=name_last1)

#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email3,
#                            password=password1,
#                            name_first=name_first1,
#                            name_last=name_last1)

# # Email address cannot be registered twice
# def test_auth_register_repeated_email(get_new_user_detail_1,
#                                       get_new_user_detail_2):

#     # Get user 1 and register them
#     email1, password1, name_first1, name_last1 = get_new_user_detail_1
#     _, _ = auth.auth_register(email=email1,
#                               password=password1,
#                               name_first=name_first1,
#                               name_last=name_last1)

#     # Get user 2
#     _, password2, name_first2, name_last2 = get_new_user_detail_2

#     # Register user 2 with the same email as user 1
#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email1,
#                            password=password2,
#                            name_first=name_first2,
#                            name_last=name_last2)

# # Test case for password less than 6 char
# def test_auth_register_invalid_password(get_new_user_detail_1):

#     # Get user 1
#     email, password, name_first, name_last = get_new_user_detail_1

#     # Invalidate the password
#     invalid_password = password[:5]

#     # Password less than 6 char raises InputError
#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email,
#                            password=invalid_password,
#                            name_first=name_first,
#                            name_last=name_last)

# # Ensure that name_first and name_last are both between 1 and 50 characters in length
# def test_auth_register_invalid_name(get_new_user_detail_1,
#                                     get_invalid_user_name):

#     # Get the user information
#     email, password, name_first, name_last = get_new_user_detail_1
#     invalid_name_long, invalid_name_empty = get_invalid_user_name

#     # Test invalid first name only
#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email,
#                            password=password,
#                            name_first=invalid_name_long,
#                            name_last=name_last)

#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email,
#                            password=password,
#                            name_first=invalid_name_empty,
#                            name_last=name_last)

#     # Test invalid last name only
#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email,
#                            password=password,
#                            name_first=name_first,
#                            name_last=invalid_name_long)

#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email,
#                            password=password,
#                            name_first=name_first,
#                            name_last=invalid_name_empty)

#     # Test invalid first name and last name
#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email,
#                            password=password,
#                            name_first=invalid_name_long,
#                            name_last=invalid_name_empty)

#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email,
#                            password=password,
#                            name_first=invalid_name_empty,
#                            name_last=invalid_name_long)

#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email,
#                            password=password,
#                            name_first=invalid_name_long,
#                            name_last=invalid_name_long)

#     with pytest.raises(error.InputError):
#         auth.auth_register(email=email,
#                            password=password,
#                            name_first=invalid_name_empty,
#                            name_last=invalid_name_empty)

# # test for correct handle generation
# def test_auth_register_handle(get_new_user_detail_1, get_new_user_detail_2,
#                               get_new_user_detail_3):

#     # register user 1
#     email1, password1, name_first1, name_last1 = get_new_user_detail_1
#     u_id1, token1 = auth.auth_register(email=email1,
#                                        password=password1,
#                                        name_first=name_first1,
#                                        name_last=name_last1)

#     # check for correct handle for user 1
#     assert user.user_profile(
#         token1,
#         u_id1)['user']['handle_str'] == (name_first1 + name_last1).lower()

#     # register user 2 for same name as user 1
#     email2, password2, _, _ = get_new_user_detail_2
#     u_id2, token2 = auth.auth_register(email=email2,
#                                        password=password2,
#                                        name_first=name_first1,
#                                        name_last=name_last1)

#     # check for correct handle for user 2
#     assert user.user_profile(
#         token2, u_id2)['user']['handle_str'] == (name_first1 +
#                                                  name_last1).lower() + u_id2

#     # register user 3
#     email3, password3, _, _ = get_new_user_detail_3
#     u_id3, token3 = auth.auth_register(email=email3,
#                                        password=password3,
#                                        name_first=name_first1,
#                                        name_last=name_last1)

#     # check for correct handle for user 3
#     assert user.user_profile(
#         token3, u_id2)['user']['handle_str'] == (name_first1 +
#                                                  name_last1).lower() + u_id3
