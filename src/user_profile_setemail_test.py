#Raymond: Tests for user_profile_setemail function


import pytest
import user
import user_test_helper
import error
import auth

def test_user_profile_setemail():
#Setup
    #Register test user 1
    user_id, token = user_test_helper.get_new_user1()

#Actual test
    user.user_profile_setemail(token, 'z1111111x@unsw.edu.au')
    assert user.user_profile(token, user_id) == {
        'user': {
        	'u_id': 1,
        	'email': 'z1111111x@unsw.edu.au',
        	'name_first': 'James',
        	'name_last': 'Bond',
        	'handle_str': 'jbond',
        },
    }

#Clean up (if necessary)
    pass

def test_user_profile_setemail_email_not_valid():
#Setup
    #Register test user 1
    token = user_test_helper.get_new_user1()[1]

#Actual test
    with pytest.raises(error.InputError):
        user.user_profile_setemail(token, 'z1111111x.unsw.edu.au')
        user.user_profile_setemail(token, 'z!#$%^&*()@unsw.edu.au')
        user.user_profile_setemail(token, 'z1111111xunsweduau')

#Clean up (if necessary)
    pass

def test_user_profile_setemail_email_already_used():
#Setup
    #Register test user 1
    token = user_test_helper.get_new_user1()[1]

    #Logout test user 1
    auth.auth_logout(token)

    #Register test user 2
    token = user_test_helper.get_new_user2()[1]
#Actual test
    with pytest.raises(error.InputError):
        user.user_profile_setemail(token, 'z1111111@unsw.edu.au')

#Clean up (if necessary)
    pass
