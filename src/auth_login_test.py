'''
Notes:
1. Think what possible case you want to test in real life, and simulate that in the test
2. Normally use import <filename> and then use filename.function()
3. Assume functions are working 
4. Make sure test are usable for iteration 2 & 3
5. Don't worry about clean up in iteratin 1
6. Go for minimum number of tests maximum coverage

'''
from error import InputError
import pytest
import auth
import re   #Regular Expression Module

@pytest.fixture
def get_new_user():  
    # dummy data
    email = "z1234567@unsw.edu.au"
    password = "qwetyu"
    name_first = "Zhihan"
    name_last = "Qin"
    data = auth.auth_register(email, password, name_first, name_last)  
    return data['u_id'], data['token'], email, password

# check if the email form is correct or not
def check_email_form(email):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    # pass the regualar expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        return True           
    else:  
        return False

# ensure that valid user can login successfully
def test_login(get_new_user):
    ############## SET UP STATE ##############################
    # valid u_id and token *we don't care about token*
    u_id, token, email, password = get_new_user

    # log user we just created out
    auth.auth_logout(token)

    ############## ACTUAL TEST ###############################
    login_retval  = auth.auth_login(email, password)
    test_u_id = login_retval['u_id']
    
    assert(u_id == test_u_id)

    ############## CLEAN UP (if necessary) ###################
    pass

# ensure that valid user can login more than once simultaneously
def test_login_already_logged_in(get_new_user):
    ############## SET UP STATE ##############################
    # valid u_id and token *we don't care about token*
    u_id, _, email, password = get_new_user

    ############## ACTUAL TEST ###############################
    login_retval  = auth.auth_login(email, password)
    test_u_id = login_retval['u_id']
    
    assert(u_id != test_u_id)

    ############## CLEAN UP (if necessary) ###################
    pass

#ensure that the input email is valid
def test_invalid_email_form():
    ############## SET UP STATE ##############################
    invalid_email = "z1234567.unsw.edu.au"
    password = "qwetyu"

    ############## ACTUAL TEST ###############################
    if(check_email_form(invalid_email) != True):
        with pytest.raises(InputError):
            auth.auth_login(invalid_email, password)        

    ############## CLEAN UP (if necessary) ###################
    pass 

#ensure that the input email is already registered
def test_non_registered_email():
    ############## SET UP STATE ##############################
    not_registered_email = "z7654321@unsw.edu.au"
    password = "qwetyu"

    ############## ACTUAL TEST ###############################
    with pytest.raises(InputError):
        auth.auth_login(not_registered_email, password)

    ############## CLEAN UP (if necessary) ###################
    pass

#ensure that the input password is correct
def test_wrong_password(get_new_user):
    ############## SET UP STATE ##############################
    # valid u_id and token *we don't care about token*
    _, token, email, password = get_new_user

    # log user we just created out
    auth.auth_logout(token)

    wrongly_inputed_password = "wetyulcd"

    ############## ACTUAL TEST ###############################
    if(password != wrongly_inputed_password):
        with pytest.raises(InputError):
            auth.auth_login(email, wrongly_inputed_password)

    ############## CLEAN UP (if necessary) ###################
    pass