#Raymond: Tests for user_profile_sethandle function

import pytest
import user
import user_test_helper
import error
import auth

def test_user_profile_sethandle():
#Setup
    #Register test user 1
    user_id, token = user_test_helper.get_new_user1()

#Actual test
    user.user_profile_sethandle(token, 'jbond007')
    assert user.user_profile(token, user_id) == {
        'user': {
        	'u_id': 1,
        	'email': 'z1111111@unsw.edu.au',
        	'name_first': 'James',
        	'name_last': 'Bond',
        	'handle_str': 'jbond007',
        },
    }

#Clean up (if necessary)
    pass

def test_user_profile_sethandle_handle_not_valid():
#Setup
    #Register test user 1
    token = user_test_helper.get_new_user1()[1]

#Actual test
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token, '')
        user.user_profile_sethandle(token, 'j')
        user.user_profile_sethandle(token, 'jb')
        user.user_profile_sethandle(token, 'jamesbondthegreatofau')


#Clean up (if necessary)
    pass

def test_user_profile_sethandle_handle_already_used():
#Setup
    #Register test user 1
    token = user_test_helper.get_new_user1()[1]

    #Log our test user 1
    auth.auth_logout(token)

    #Register test user 2
    token = user_test_helper.get_new_user2()[1]
#Actual test
    with pytest.raises(error.InputError):
        user.user_profile_sethandle(token, 'jbond')

#Clean up (if necessary)
    pass