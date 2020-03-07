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
    channel_id = channels.channels_create(token1, channel_name, True)
    # Test there is no match here
    assert other.search(token1, "no match") == {'messages' : []}

# Test a single user who has joined a channel with a message but the query does not match.
def test_single_user_one_channel_message_no_match():
    # Register person one
    person_one, token1 = create_person_one()
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token1, channel_name, True)

    sentence = 'The quick brown fox jumps over the lazy dog'
    # Send message
    message.message_send(token1, channel_id, sentence)
    # Test there is no match
    assert other.search(token1, "no match") == {'messages' : []}

# Test a single user who has created a channel with a message and query matches.
def test_single_user_one_channel_message_match():
    # Register person one
    person_one, token1 = create_person_one()
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token1, channel_name, True)

    sentence = 'The quick brown fox jumps over the lazy dog'
    # Send message
    stored_message = message.message_send(token1, channel_id, sentence)

    # Test there is a match
    assert other.search(token1, sentence) == {'messages' : [stored_message]}

# Test a single user who has created a channel with two messages, one match.
def test_single_user_channel_one_match():
    # Register person one
    person_one, token1 = create_person_one()
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token1, channel_name, True)

    sentence1 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    stored_message1 = message.message_send(token1, channel_id, sentence1)

    sentence2 = 'Hello world'
    # Send message
    stored_message2 = message.message_send(token1, channel_id, sentence2)

    # Test there is a match
    assert other.search(token1, sentence1) == {'messages' : [stored_message1]}

# Test a single user who has created a channel with two messages, two match.
def test_single_user_channel_two_match():
    # Register person one
    person_one, token1 = create_person_one()
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token1, channel_name, True)

    sentence1 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    stored_message1 = message.message_send(token1, channel_id, sentence1)

    sentence2 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    stored_message2 = message.message_send(token1, channel_id, sentence2)

    # Test there is a match
    # The set is a neat trick to ensure order does not matter
    assert set(other.search(token1, sentence1)['messages']) == set(stored_message1, stored_message2)

# Test a single user who has created two channels, no match.
def test_single_user_channels_no_match():
    # Register person one
    person_one, token1 = create_person_one()
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id1 = channels.channels_create(token1, channel_name, True)

    # Create test channel 2
    channel_name = 'Test Channe2'    
    is_public = True
    channel_id2 = channels.channels_create(token1, channel_name, True)

    sentence1 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    stored_message1 = message.message_send(token1, channel_id1, sentence1)

    sentence2 = 'Hello word'
    # Send message
    stored_message2 = message.message_send(token1, channel_id2, sentence2)

    # Assert no matches
    assert other.search(token1, "no match") == {'messages' : []}

    # Test a single user who has created two channels, one match.
def test_single_user_channels_one_match():
    # Register person one
    person_one, token1 = create_person_one()
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id1 = channels.channels_create(token1, channel_name, True)

    # Create test channel 2
    channel_name = 'Test Channe2'    
    is_public = True
    channel_id2 = channels.channels_create(token1, channel_name, True)

    sentence1 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    stored_message1 = message.message_send(token1, channel_id1, sentence1)

    sentence2 = 'Hello word'
    # Send message
    stored_message2 = message.message_send(token1, channel_id2, sentence2)
    
    # Assert no matches
    assert other.search(token1, sentence1) == {'messages' : [stored_message1]}

    # Test a single user who has created two channels, two match.
def test_single_user_channels_two_match():
    # Register person one
    person_one, token1 = create_person_one()
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id1 = channels.channels_create(token1, channel_name, True)

    # Create test channel 2
    channel_name = 'Test Channe2'    
    is_public = True
    channel_id2 = channels.channels_create(token1, channel_name, True)

    sentence1 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    stored_message1 = message.message_send(token1, channel_id1, sentence1)

    sentence2 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    stored_message2 = message.message_send(token1, channel_id2, sentence2)
    
    # Assert no matches
    assert set(other.search(token1, sentence1)['messages']) == set(stored_message1, stored_message2)


# Now we will test multiple people. 

    # Test two people who joined a channel (owner is person1), one message sent by person2 and matches person1's query
def test_users_channel_match():
    # Register person one
    person_one, token1 = create_person_one()

    # Register person two
    person_two, token2 = create_person_two()

    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id1 = channels.channels_create(token1, channel_name, True)

    # Add person 2 to channel 1
    channels.channel_join(token2, channel_id1)

    # Send message by person 2
    sentence1 = 'The quick brown fox jumps over the lazy dog'
    stored_message1 = message.message_send(token2, channel_id1, sentence1)

    # Ensure when person 1 searches, we get a match
    assert other.search(token1, sentence1) == {'messages' : [stored_message1]}

    # Test two people who make two different channels, one message sent by person2 and matches person1's query.
    # There should be no match since this is different channels.
def test_users_channels_match():
    # Register person one
    person_one, token1 = create_person_one()

    # Register person two
    person_two, token2 = create_person_two()

    # Create test channel 1 with person 1
    channel_name1 = 'Test Channel1'    
    is_public = True
    channel_id1 = channels.channels_create(token1, channel_name1, True)

    # Create test channel 2 with person 2
    channel_name2 = 'Test Channel2'    
    is_public = True
    channel_id2 = channels.channels_create(token2, channel_name2, True)

    # Send message with person 2 to channel 2
    sentence1 = 'The quick brown fox jumps over the lazy dog'
    stored_message1 = message.message_send(token2, channel_id2, sentence1)

    # Assert person 1 has no search involving this sentence. Even if we search this query
    assert other.search(token1, sentence1) == {'messages' : []}
