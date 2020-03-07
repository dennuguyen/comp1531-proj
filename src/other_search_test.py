import pytest
import auth
import message
import channels

# TODO: Check invalid token?

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

# First test will test for a single user that has not joined a channel
def test_single_user_no_channel():
    # Register person one
    person_one, token1 = create_person_one()
    # This should return a dictionary with an empty list under the 'messages' key.
    assert other.search(token1, "no match") == {'messages' : []}

# Test a single user who has joined a channel with no messages in it should return the same as above.
def test_single_user_one_channel_no_message():
    # Register person one
    person_one, token1 = create_person_one()
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token, channel_name, True)
    # Test there is no match here
    assert other.search(token1, "no match") == {'messages' : []}

