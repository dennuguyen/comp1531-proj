import auth
import other
import pytest

# Creating dummy data

def create_person_one():
    # Returns dictionary and token of person 1
    person_one = {}
    u_id1, token1 = auth.auth_register('person1@unsw.com', 'password', 'First', 'Person')
    person_one['u_id'] = u_id1
    person_one['email'] = 'person1@unsw.com'
    person_one['name_first'] = 'First'
    person_one['name_last'] = 'Person'
    person_one['handle_str'] = 'firstperson'
    return person_one, token1
    
def create_person_two():
    # Returns dictionary and token of person 2
    person_two = {}
    u_id1, token1 = auth.auth_register('person2@unsw.com', 'password', 'Second', 'Person')
    person_two['u_id'] = u_id2
    person_two['email'] = 'person2@unsw.com'
    person_two['name_first'] = 'Second'
    person_two['name_last'] = 'Person'
    person_two['handle_str'] = 'secondperson'
    return person_two, token2

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