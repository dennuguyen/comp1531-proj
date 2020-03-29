import data
import auth
import other
import pytest
import sys
sys.path.append('../')


def create_person_one(get_new_user_1, get_new_user_detail_1):
    # Returns dictionary and token of person 1
    u_id, token = get_new_user_1
    email, _, name_first, name_last = get_new_user_detail_1
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
    email, _, name_first, name_last = get_new_user_detail_2
    person_two = {}
    person_two['u_id'] = u_id
    person_two['email'] = email
    person_two['name_first'] = name_first
    person_two['name_last'] = name_last
    person_two['handle_str'] = name_first.lower() + name_last.lower()
    return person_two, token


def test_users_all_one_person(get_new_user_1, get_new_user_detail_1):
    # Create person one
    person_one, token1 = create_person_one(
        get_new_user_1, get_new_user_detail_1)
    # Now test making person_one a list.
    assert other.users_all(token=token1) == {'users': [person_one]}

    data.get_data().reset()

def test_users_all_two_people(get_new_user_1, get_new_user_detail_1,
                              get_new_user_2, get_new_user_detail_2):

    # Create person one
    person_one, token1 = create_person_one(
        get_new_user_1, get_new_user_detail_1)

    # Create person two
    person_two, _ = create_person_two(get_new_user_2, get_new_user_detail_2)

    # Now test making people into a list.

    # I have done this using sets since, each person is unique by their u_id
    # also sets are un-ordered. It lets me removed the assumpion in which way
    # people will be added to the output of users_all

    # output_users_all = set(other.users_all(token)['users'])
    # comparison = set(person_one, person_two)
    # assert output_users_all == comparison

    output_users_all = other.users_all(token=token1)['users']
    comparison = (person_one, person_two)

    flag = 0
    for a in output_users_all:
        for b in comparison:
            if (a == b):
                flag += 1
    assert flag == len(output_users_all)

    data.get_data().reset()