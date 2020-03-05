#Raymond: Tests for user_profile_setname function

import pytest
import user
import user_test_helper
import error


def test_user_profile_setname():
    #Setup
        #Register test user 1
    user_id, token = user_test_helper.get_new_user1()

    #Actual test
    user.user_profile_setname(token, 'Ted', 'Bundy')
    assert user.user_profile(token, user_id) == {
        'user': {
        	'u_id': 1,
        	'email': 'z1111111@unsw.cedu.au',
        	'name_first': 'Ted',
        	'name_last': 'Bundy',
        	'handle_str': 'jbond',
        },
    }

    #Clean up (if necessary)
    pass

def test_user_profile_setname_name_not_valid():
    #Setup
        #Register test user 1
    token = user_test_helper.get_new_user1()[1]

    #Actual test
    with pytest.raises(error.InputError):
        user.user_profile_setname(token, '', 'Bundy')
        user.user_profile_setname(token, 'Ted', '')
        user.user_profile_setname(token, '', '')
        user.user_profile_setname(token, 'T'*51, 'Bundy')
        user.user_profile_setname(token, 'Ted', 'B'*51)
        user.user_profile_setname(token, 'T'*51, 'B'*51)

    #Clean up (if necessary)
    pass