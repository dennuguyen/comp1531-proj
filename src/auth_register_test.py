import auth
import pytest
from error import InputError
from auth_login_test import get_new_user, check_email_form

@pytest.fixture(scope="module")
def gen_person_info():
    # dummy data
    email = "z1234567@unsw.edu.au"
    password = "qwetyu"
    name_first = "Zhihan"
    name_last = "Qin"

    return email, password, name_first, name_last

#ensure that a person with valid infomation can register
def test_register(gen_person_info):
    ############## SET UP STATE ##############################
    email, password, name_first, name_last = gen_person_info
    
    ############## ACTUAL TEST ###############################
    #register
    register_retval = auth.auth_register(email, password, name_first, name_last)
    test_u_id = register_retval['u_id']
    test_token = register_retval['token']

    assert(test_u_id == 1 and test_token == '12345')
    ############## CLEAN UP (if necessary) ###################
    pass

#ensure that the input email is valid
def test_invalid_email_form():
    ############## SET UP STATE ##############################
    invalid_email = "z1234567.unsw.edu.au"
    password = "qwetyu"
    name_first = "Zhihan"
    name_last = "Qin"

    ############## ACTUAL TEST ###############################
    if(check_email_form(invalid_email) != True):
        with pytest.raises(InputError):
            auth.auth_register(invalid_email, password, name_first, name_last)        

    ############## CLEAN UP (if necessary) ###################
    pass


#ensure that an email address cannot be registered twice
def test_repeated_email_form(get_new_user):
    ############## SET UP STATE ##############################
    _, _, email, _ = get_new_user

    another_email = "z1234567@unsw.edu.au"
    another_password = 'asdfghj'
    another_name_first = 'Taylor'
    another_name_last = 'Swift'

    ############## ACTUAL TEST ###############################  
    if(another_email == email):
        with pytest.raises(InputError):
            auth.auth_register(email, another_password, another_name_first, another_name_last)

    ############## CLEAN UP (if necessary) ###################
    pass

#ensure that Password entered is less than 6 characters long
def test_valid_Password():
    ############## SET UP STATE ##############################
    email = "z1234567@unsw.edu.au"
    invalid_password = "qwety"
    name_first = "Zhihan"
    name_last = "Qin"

    ############## ACTUAL TEST ###############################  
    if(len(invalid_password) < 6):
        with pytest.raises(InputError):
            auth.auth_register(email, invalid_password, name_first, name_last)

    ############## CLEAN UP (if necessary) ###################
    pass

#ensure that name_first and name_last are both between 1 and 50 characters in length
def test_valid_name():
    ############## SET UP STATE ##############################
    email = "z1234567@unsw.edu.au"
    password = "qwetyz"
    invalid_name_first = "zaqwertyuioplmnbvcxsdfghjklpoiuytrewqazxsdcvfgbnhjmk"
    invalid_name_last = ""

    ############## ACTUAL TEST ###############################  
    if((len(invalid_name_first) > 50 or len(invalid_name_first)<1) \
        and 
        len(invalid_name_last) > 50 or len(invalid_name_last)<1):
        with pytest.raises(InputError):
            auth.auth_register(email, password, invalid_name_first, invalid_name_last)

    ############## CLEAN UP (if necessary) ###################
    pass