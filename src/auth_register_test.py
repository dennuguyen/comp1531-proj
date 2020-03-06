import auth
import pytest
import other
from error import InputError
from auth_login_test import get_new_user, check_email_form

@pytest.fixture(scope = 'module')
def gen_person_info():
    # dummy data
    email1 = 'z1234567@unsw.edu.au'
    email2 = 'z1234567@gmail.com'
    password = 'qwetyu231'
    name_first = 'Zhihan'
    name_last = 'Qin'
    invalid_name_first = 'zaqwertyuioplmnbvcxsdfghjklpoiuytrewqazxsdcvfgbnhjmk'
    invalid_name_last = ''

    return email1, email2, password, name_first, name_last, invalid_name_first, invalid_name_last

# basic case
def test_auth_register(gen_person_info):
    email1, _, password, name_first, name_last, _, _ = gen_person_info

    # register and unpack u_id and token
    auth_dict = auth.auth_register(email1, password, name_first, name_last)
    u_id = dictionary['u_id']
    token = dictionary['token']

    # create user_dict
    user_dict = {
        'user': {
        	'u_id': u_id,
        	'email': email1,
        	'name_first': name_first,
        	'name_last': name_last,
        	'handle_str': (name_first + name_last).lower(), # makes string all lower case
        },
    }

    # check if user exists after register
    assert user_profile(token, u_id) == user_dict

# check email validity
def test_auth_register_invalid_email(gen_person_info):
    email1, _, password, name_first, name_last, _, _ = gen_person_info

    email1.replace('@', '.') # string is now "z1234567.unsw.edu.au"

    with pytest.raises(InputError):
        auth.auth_register(email1, password, name_first, name_last)

# email address cannot be registered twice
def test_auth_register_repeated_email(gen_person_info):
    email1, _, password, name_first, name_last, _, _ = gen_person_info

    auth.auth_register(email1, password, name_first, name_last)

    # try registering again
    with pytest.raises(InputError):
        auth.auth_register(email1, password, name_first, name_last)

# test case for password less than 6 char
def test_auth_register_invalid_password(gen_person_info):
    email1, _, password, name_first, name_last, _, _ = gen_person_info
    password = password[:5]

    # password less than 6 char raises InputError
    with pytest.raises(InputError):
        auth.auth_register(email1, password, name_first, name_last)

# ensure that name_first and name_last are both between 1 and 50 characters in length
def test_auth_register_invalid_name(gen_person_info):
    email1, email2, password, name_first, name_last, invalid_name_first, invalid_name_last = gen_person_info

    assert len(invalid_name_first) >= 50
    assert len(invalid_name_last)  == 0

    # test invalid first name only
    with pytest.raises(InputError):
        auth.auth_register(email1, password, invalid_name_first, name_last)

    # test invalid last name only
    with pytest.raises(InputError):
        auth.auth_register(email2, password, name_first, invalid_name_last)
