import pytest

def test_pytest_fixture(get_new_user, gen_person_info):

    email, password, name_first, name_last = get_new_user
    email1, email2, password, name_first, name_last, invalid_name_first, invalid_name_last = gen_person_info
    
    assert email == "z1234567@unsw.edu.au"
    assert email1 == 'z1234567@unsw.edu.au'
    return

def add_int_to_string():

    for integer in range(1,4):
        message = 'test message ' + f'{integer}'
        print(message)
        integer += 1

add_int_to_string()

