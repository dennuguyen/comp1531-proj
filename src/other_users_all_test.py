import auth
import other
import pytest

# TODO: Check invalid token?

# Creating dummy data

def create_person_one(get_new_user_1, get_new_user_detail_1):
    # Returns dictionary and token of person 1
    u_id, token = get_new_user_1
    email, password, name_first, name_last = get_new_user_detail_1
    person_one = {}
    person_one['u_id'] = u_id
    person_one['email'] = email
    person_one['name_first'] = name_first
    person_one['name_last'] = name_last
    person_one['handle_str'] = name_first.lower() + name_last.lower()
    return person_one, token
    
def create_person_two(get_new_user_2, get_new_user_detail_2):
    # Returns dictionary and token of person 1
    u_id, token = get_new_user_2
    email, password, name_first, name_last = get_new_user_detail_2
    person_one = {}
    person_one['u_id'] = u_id
    person_one['email'] = email
    person_one['name_first'] = name_first
    person_one['name_last'] = name_last
    person_one['handle_str'] = name_first.lower() + name_last.lower()
    return person_two, token

def test_users_all_one_person():
    # Create person one
    person_one, token1 = create_person_one()
    # Now test making person_one a list.
    assert other.users_all(token1) == {'users': [person_one]}

def test_users_all_two_people():
    # Create person one
    person_one, token1 = create_person_one()
    # Create person two
    person_two, token2 = create_person_two()
    
    # Now test making people into a list.

    # I have done this using sets since, each person is unique by their u_id
    # also sets are un-ordered. It lets me removed the assumpion in which way 
    # people will be added to the output of users_all 
    output_users_all = set(other.users_all(token)['users'])
    comparison = set(person_one, person_two)
    assert output_users_all == comparison