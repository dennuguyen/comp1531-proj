import pytest
import channels
import auth

# for auth_login_test.py & auth_logout_test.py
def get_new_user():
    email = "z1234567@unsw.edu.au"
    password = "qwetyu"
    name_first = "Zhihan"
    name_last = "Qin"

    return email, password, name_first, name_last

# for auth_register_test.py
@pytest.fixture(scope="session")
def gen_person_info():
    email1, password, name_first, name_last= get_new_user()

    email2 = 'z1234567@gmail.com'
    invalid_name_first = 'zaqwertyuioplmnbvcxsdfghjklpoiuytrewqazxsdcvfgbnhjmk'
    invalid_name_last = ''

    return email1, email2, password, name_first, name_last, invalid_name_first, invalid_name_last

# for channel test
@pytest.fixture(scope="session")
def get_new_user_1():
    email = "owner@unsw.com"
    password = "password"
    name_first = "The"
    name_last = "Owner"
    return auth.auth_register(email, password, name_first, name_last)

# for channel test
@pytest.fixture(scope="session")
def get_new_user_2():
    email = "stranger@unsw.com"
    password = "password"
    name_first = "A"
    name_last = "Stranger"
    return auth.auth_register(email, password, name_first, name_last)

