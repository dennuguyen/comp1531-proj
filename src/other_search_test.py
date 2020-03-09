import pytest
import auth
import message
import channels
import other
import channel

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
    person_two = {}
    person_two['u_id'] = u_id
    person_two['email'] = email
    person_two['name_first'] = name_first
    person_two['name_last'] = name_last
    person_two['handle_str'] = name_first.lower() + name_last.lower()
    return person_two, token

# First test will test for a single user that has not joined a channel
def test_single_user_no_channel(get_new_user_1, get_new_user_detail_1):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)
    # This should return a dictionary with an empty list under the 'messages' key.
    assert other.search(token1, "no match") == {'messages' : []}

# Test a single user who has joined a channel with no messages in it should return the same as above.
def test_single_user_one_channel_no_message(get_new_user_1, get_new_user_detail_1):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token1, channel_name, True)
    # Test there is no match here
    assert other.search(token1, "no match") == {'messages' : []}

# Test a single user who has joined a channel with a message but the query does not match.
def test_single_user_one_channel_message_no_match(get_new_user_1, get_new_user_detail_1):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)
    
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
def test_single_user_one_channel_message_match(get_new_user_1, get_new_user_detail_1):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token1, channel_name, True)

    sentence = 'The quick brown fox jumps over the lazy dog'
    # Send message
    message.message_send(token1, channel_id, sentence)

    # Test there is a match
    assert other.search(token1, sentence)['messages'][0]['message'] == sentence

# Test a single user who has created a channel with two messages, one match.
def test_single_user_channel_one_match(get_new_user_1, get_new_user_detail_1):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token1, channel_name, True)

    sentence1 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    message.message_send(token1, channel_id, sentence1)

    sentence2 = 'Hello world'
    # Send message
    message.message_send(token1, channel_id, sentence2)

    # Test there is a match
    assert other.search(token1, sentence1)['messages'][0]['message'] == sentence1

# Test a single user who has created a channel with two messages, two match.
def test_single_user_channel_two_match(get_new_user_1, get_new_user_detail_1):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)
    
    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id = channels.channels_create(token1, channel_name, True)

    sentence1 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    message.message_send(token1, channel_id, sentence1)

    sentence2 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    message.message_send(token1, channel_id, sentence2)

    # Test there is two matches
    first_message = other.search(token1, sentence1)['messages'][0]['message'] == sentence1
    second_message = other.search(token1, sentence1)['messages'][1]['message'] == sentence2
    assert first_message and second_message

# Test a single user who has created two channels, no match.
def test_single_user_channels_no_match(get_new_user_1, get_new_user_detail_1):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)
    
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
    message.message_send(token1, channel_id1, sentence1)

    sentence2 = 'Hello word'
    # Send message
    message.message_send(token1, channel_id2, sentence2)

    # Assert no matches
    assert other.search(token1, "no match") == {'messages' : []}

    # Test a single user who has created two channels, one match.
def test_single_user_channels_one_match(get_new_user_1, get_new_user_detail_1):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)
    
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
    message.message_send(token1, channel_id1, sentence1)

    sentence2 = 'Hello word'
    # Send message
    message.message_send(token1, channel_id2, sentence2)
    
    # Assert no matches
    assert other.search(token1, sentence1)['messages'][0]['message'] == sentence1

    # Test a single user who has created two channels, two match.
def test_single_user_channels_two_match(get_new_user_1, get_new_user_detail_1):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)
    
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
    message.message_send(token1, channel_id1, sentence1)

    sentence2 = 'The quick brown fox jumps over the lazy dog'
    # Send message
    message.message_send(token1, channel_id2, sentence2)
    
    first_message = other.search(token1, sentence1)['messages'][0]['message'] == sentence1
    second_message = other.search(token1, sentence1)['messages'][1]['message'] == sentence2
    assert first_message and second_message


# Now we will test multiple people. 

    # Test two people who joined a channel (owner is person1), one message sent by person2 and matches person1's query
def test_users_channel_match(get_new_user_1, get_new_user_detail_1, get_new_user_2, get_new_user_detail_2):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)

    # Register person two
    person_two, token2 = create_person_two(get_new_user_2, get_new_user_detail_2)

    # Create test channel 1
    channel_name = 'Test Channel1'    
    is_public = True
    channel_id1 = channels.channels_create(token1, channel_name, True)

    # Add person 2 to channel 1
    channel.channel_join(token2, channel_id1)

    # Send message by person 2
    sentence1 = 'The quick brown fox jumps over the lazy dog'
    message.message_send(token2, channel_id1, sentence1)

    # Ensure when person 1 searches, we get a match
    assert other.search(token1, sentence1)['messages'][0]['message'] == sentence1

    # Test two people who make two different channels, one message sent by person2 and matches person1's query.
    # There should be no match since this is different channels.
def test_users_channels_match(get_new_user_1, get_new_user_detail_1, get_new_user_2, get_new_user_detail_2):
    # Register person one
    person_one, token1 = create_person_one(get_new_user_1, get_new_user_detail_1)

    # Register person two
    person_two, token2 = create_person_two(get_new_user_2, get_new_user_detail_2)

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
    message.message_send(token2, channel_id2, sentence1)

    # Assert person 1 has no search involving this sentence. Even if we search this query
    assert other.search(token1, sentence1) == {'messages' : []}
