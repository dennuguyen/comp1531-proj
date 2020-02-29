#Raymond:tests for user.py

from user import profile
from user import profile_setname
from user import profile_setemail
from user import profile_sethandle

def test_profile():
    assert profile('12345', 1) == {
        'user': {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs',
        }
    }
    pass

def test_profile_setname():
    assert profile_setname('12345', 'Raymond', 'Soedargo') == {}
    pass

def test_profile_setemail():
    assert profile_setemail('12345', 'z3063670@student.unsw.edu.au') == {}
    pass

def test_profile_sethandle():
    assert profile_sethandle('12345', 'rsoedargo') == {}
    pass
