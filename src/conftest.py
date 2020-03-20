# get_new_user_detail gets the root information used to register a user
# get_new_user gets the u_id and token after registering a user

import pytest
import auth
import sys
sys.path.append('../')


@pytest.fixture(scope="session")
def get_new_user_detail_0():
    email = "john_doe@unsw.com"
    password = "password1234"
    name_first = "John"
    name_last = "Doe"

    return email, password, name_first, name_last


@pytest.fixture(scope="session")
def get_new_user_detail_1():
    email = "hugh_jackman@unsw.com"
    password = "strong password"
    name_first = "Hugh"
    name_last = "Jackman"

    return email, password, name_first, name_last


@pytest.fixture(scope="session")
def get_new_user_detail_2():
    email = "ted_bundy@unsw.com"
    password = "AJkh28aH2k21l!"
    name_first = "Ted"
    name_last = "Bundy"

    return email, password, name_first, name_last


@pytest.fixture(scope="session")
def get_new_user_detail_3():
    email = "king_kong@unsw.com"
    password = "2134oplka"
    name_first = "King"
    name_last = "Kong"

    return email, password, name_first, name_last


@pytest.fixture(scope="session")
def get_new_user_detail_4():
    email = "toocool4school@unsw.com"
    password = "p455w0rd"
    name_first = "Kid"
    name_last = "Kyle"

    return email, password, name_first, name_last


@pytest.fixture(scope="session")
def get_new_user_0(get_new_user_detail_0):
    email, password, name_first, name_last = get_new_user_detail_0
    retval = auth.auth_register(email=email,
                                password=password,
                                name_first=name_first,
                                name_last=name_last)

    return retval['u_id'], retval['token']


@pytest.fixture(scope="session")
def get_new_user_1(get_new_user_detail_1):
    email, password, name_first, name_last = get_new_user_detail_1
    retval = auth.auth_register(email=email,
                                password=password,
                                name_first=name_first,
                                name_last=name_last)

    return retval['u_id'], retval['token']


@pytest.fixture(scope="session")
def get_new_user_2(get_new_user_detail_2):
    email, password, name_first, name_last = get_new_user_detail_2
    retval = auth.auth_register(email=email,
                                password=password,
                                name_first=name_first,
                                name_last=name_last)

    return retval['u_id'], retval['token']


@pytest.fixture(scope="session")
def get_new_user_3(get_new_user_detail_3):
    email, password, name_first, name_last = get_new_user_detail_3
    retval = auth.auth_register(email=email,
                                password=password,
                                name_first=name_first,
                                name_last=name_last)

    return retval['u_id'], retval['token']


@pytest.fixture(scope="session")
def get_new_user_4(get_new_user_detail_4):
    email, password, name_first, name_last = get_new_user_detail_4
    retval = auth.auth_register(email=email,
                                password=password,
                                name_first=name_first,
                                name_last=name_last)

    return retval['u_id'], retval['token']


@pytest.fixture(scope="session")
def get_channel_name_1():
    return 'New_test_channel1'


@pytest.fixture(scope="session")
def get_channel_name_2():
    return 'New_test_channel2'


@pytest.fixture(scope="session")
def get_channel_name_3():
    return 'New_test_channel3'


@pytest.fixture(scope="session")
def get_channel_name_4():
    return 'New_test_channel4'


@pytest.fixture(scope="session")
def get_invalid_user_name():
    invalid_name_long = 'T' * 51
    invalid_name_empty = ''
    return invalid_name_long, invalid_name_empty
