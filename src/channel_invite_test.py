import pytest
import channel
import error
import channels
import auth

# Test environment
@pytest.fixture(scope="module")
def test_environment(get_new_user_1, get_new_user_2, get_new_user_3, get_new_user_4):
    u_id1, token1 = get_new_user_3
    u_id2, token2 = get_new_user_2
    u_id3, token3 = get_new_user_1
    u_id4, token4 = get_new_user_4

    return u_id1, token1, u_id2, token2, u_id3, token3, u_id4, token4

def test_channel_invite_user(test_environment):
# Setup
    u_id = test_environment[0]
    token = test_environment[1]
    u_id2 = test_environment[2]
    token2 = test_environment[3]

    ch_id = channels.channels_create(token, 'Test channel1', True)['channel_id']

# Actual test
    # The owner invites the user to new channel
    assert channel.channel_invite(token, ch_id, u_id2) == {}
    assert channels.channels_list(token2) == {'channels': [{'channel_id' : ch_id, 'name' : 'Test channel1'}]}
     
def test_channel_invite_himself(test_environment):        

    u_id = test_environment[0]
    token = test_environment[1]
    ch_id = channels.channels_create(token, 'Test channel1', True)['channel_id']

    assert channel.channel_invite(token, ch_id, u_id) == {}
    assert channels.channels_list(token) == {'channels': [{'channel_id' : ch_id, 'name' : 'Test channel1'}]}

def test_channel_invite_already_member(test_environment):

    # set up environment
    u_id = test_environment[0]
    token = test_environment[1]
    u_id2 = test_environment[2]
    token2 = test_environment[3]

    ch_id = channels.channels_create(token, 'Test channel1', True)['channel_id']

    channel.channel_invite(token, ch_id, u_id2)

    # The owner invites the user to new channel
    assert channel.channel_invite(token, ch_id, u_id2) == {}
    assert channels.channels_list(token2) == {'channels': [{'channel_id' : ch_id, 'name' : 'Test channel1'}]}

def test_channel_invite_users(test_environment):
# Setup
    u_id = test_environment[0]
    token = test_environment[1]
    u_id2 = test_environment[2]
    token2 = test_environment[3]
    u_id3 = test_environment[4]
    token3 = test_environment[5]

    ch_id = channels.channels_create(token, 'Test channel1', True)['channel_id']

# Actual test
    # The owner invites the user to new channel
    assert channel.channel_invite(token, ch_id, u_id2) == {}
    assert channel.channel_invite(token, ch_id, u_id3) == {}
    assert channels.channels_list(token2) == {'channels': [{'channel_id' : ch_id, 'name' : 'Test channel1'}]}
    assert channels.channels_list(token3) == {'channels': [{'channel_id' : ch_id, 'name' : 'Test channel1'}]}

def test_channel_invite_unauthorised_user(test_environment):

    # set up environment
    u_id = test_environment[0]
    token = test_environment[1]
    u_id2 = test_environment[2]
    token2 = test_environment[3]
    u_id3 = test_environment[4]
    token3 = test_environment[5]
    u_id4 = test_environment[6]
    token4 = test_environment[7]

    ch_id = channels.channels_create(token, 'Test channel1', True)['channel_id']

    # A stranger invites the owner to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token3, ch_id, u_id)

    # A stranger invites themself to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token3, ch_id, u_id3)

    # A stranger invites the user to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token3, ch_id, u_id2)

    # A stranger invites another stranger to new channel
    with pytest.raises(error.AccessError):
        channel.channel_invite(token3, ch_id, u_id4)

def test_channel_invite_invalid_channel(test_environment):

    # set up environment
    u_id = test_environment[0]
    token = test_environment[1]
    u_id2 = test_environment[2]
    token2 = test_environment[3]

    ch_id = channels.channels_create(token, 'Test channel1', True)['channel_id']

    # invalid channel id i.e. channel does not exist
    with pytest.raises(error.InputError):
        channel.channel_invite(token, ch_id + 1, u_id2)

def test_channel_invite_invalid_user(test_environment):

    # set up environment
    u_id = test_environment[0]
    token = test_environment[1]
    u_id2 = test_environment[2]
    token2 = test_environment[3]

    ch_id = channels.channels_create(token, 'Test channel1', True)['channel_id']

    # invalid user id i.e. user does not exist
    with pytest.raises(error.InputError):
        channel.channel_invite(token, ch_id, u_id2 + 1)