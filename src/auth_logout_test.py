from auth_login_test import get_new_user
import pytest
import auth

#ensure that valid users can log out sucessfully
def test_logout(get_new_user):
############## SET UP STATE ##############################
    # valid u_id and token *we don't care about token*
    _, token, _, _ = get_new_user

    ############## ACTUAL TEST ###############################
    logout_retval  = auth.auth_logout(token)
    test_is_success = logout_retval['is_success']
    
    assert(test_is_success == True)

    ############## CLEAN UP (if necessary) ###################
    pass
