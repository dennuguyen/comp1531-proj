import pytest
import channels
import auth


# for auth.py generating a user who is going to register next
@pytest.fixture(scope="session")
def get_new_user_detail_zero():
    email = "ownerofslackrs@unsw.com"
    password = "qwetmn"
    name_first = "Ownerof"
    name_last = "Slackr"

    return email, password, name_first, name_last

def get_new_user_detail_a():
    email = "ownerofslackrs@unsw.com"
    password = "qwetls"
    name_first = "Dan"
    name_last = "Nguyen"

    return email, password, name_first, name_last

def get_new_user_detail_b():
    email = "stranger@unsw.com"
    password = "qwetla"
    name_first = "A"
    name_last = "Stranger"

    return email, password, name_first, name_last

def get_new_user_detail_c():
    email = "anotherstranger@unsw.com"
    password = "qwetrb"
    name_first = "Another"
    name_last = "Stranger"

    return email, password, name_first, name_last

def get_new_user_detail_d():
    email = "strangerzzz@unsw.com"
    password = "qwetds"
    name_first = "Two"
    name_last = "Strangerzzz"

    return email, password, name_first, name_last

@pytest.fixture(scope="session")
def gen_person_info(get_new_user):
    email1, password, name_first, name_last= get_new_user

    email2 = 'z1234567@gmail.com'
    invalid_name_first = 'zaqwertyuioplmnbvcxsdfghjklpoiuytrewqazxsdcvfgbnhjmk'
    invalid_name_last = ''

    invalid_name_first2 = ''
    invalid_name_last2 = 'zaqwertyuioplmnbvcxsdfghjklpoiuytrewqazxsdcvfgbnhjmk'

    return email1, email2, password, name_first, name_last, invalid_name_first, invalid_name_last


# for channels.py generating users who have already registered
@pytest.fixture(scope="session")
def get_new_user_0():
    email = "ownerofslackrs@unsw.com"
    password = "qwetmn"
    name_first = "Ownerof"
    name_last = "Slackr"

    retval = auth.auth_register(email, password, name_first, name_last)

    return retval['u_id'], retval['token']

def get_new_user_1():
    email = "owner@unsw.com"
    password = "qwetls"
    name_first = "The"
    name_last = "Owner"

    retval = auth.auth_register(email, password, name_first, name_last)

    return retval['u_id'], retval['token']

@pytest.fixture(scope="session")
def get_new_user_2():
    email = "stranger@unsw.com"
    password = "qwetla"
    name_first = "A"
    name_last = "Stranger"

    retval = auth.auth_register(email, password, name_first, name_last)

    return retval['u_id'], retval['token']

@pytest.fixture(scope="session")
def get_new_user_3():
    email = "anotherstranger@unsw.com"
    password = "qwetrb"
    name_first = "Another"
    name_last = "Stranger"

    retval = auth.auth_register(email, password, name_first, name_last)

    return retval['u_id'], retval['token']

@pytest.fixture(scope="session")
def get_new_user_4():
    email = "strangerzzz@unsw.com"
    password = "qwetds"
    name_first = "Two"
    name_last = "Strangerzzz"

    retval = auth.auth_register(email, password, name_first, name_last)
    
    return retval['u_id'], retval['token']


