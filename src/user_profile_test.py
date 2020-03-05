#Raymond: Tests for user_profile function

import pytest
import user
import user_test_helper
import error


def test_user_profile():
    #Setup
        #Register test user 1
    user_id, token = user_test_helper.get_new_user1()
    #Actual test
    assert user.user_profile(token, user_id) == {
        'user': {
        	'u_id': 1,
        	'email': 'z1111111@unsw.cedu.au',
        	'name_first': 'James',
        	'name_last': 'Bond',
        	'handle_str': 'jbond',
        },
    }
    #Clean up (if necessary)
    pass

def test_user_profile_invalid_uid():
    #Setup
        #Register test user 1
    user_id, token = user_test_helper.get_new_user1()
    #Actual test
    with pytest.raises(error.InputError):
        user.user_profile(token, (user_id+1))

    #Clean up (if necessary)
    pass

