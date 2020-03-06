import pytest

@pytest.fixture(scope="session")
def get_new_user():
    email = "z1234567@unsw.edu.au"
    password = "qwetyu"
    name_first = "Zhihan"
    name_last = "Qin"

    return email, password, name_first, name_last

@pytest.fixture(scope="session")
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

