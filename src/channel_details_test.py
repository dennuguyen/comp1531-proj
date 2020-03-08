import pytest
import channel
import error
import channels
import auth

@pytest.fixture(scope="module")
def test_environment(get_new_user_1, get_new_user_2, get_new_user_3):

    u_id1, token1 = get_new_user_3
    u_id2, token2 = get_new_user_1
    u_id3, token3 = get_new_user_2

    ch_id = channels.channels_create(token2, 'New Channel', True)['channel_id'] # u_id2 is owner

    return u_id1, token1, u_id2, token2, u_id3, token3, ch_id
    
def test_channel_details():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment
    channel.channel_invite(token2, ch_id, u_id1)

    correct_detail = {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id2,
                'name_first': 'The',
                'name_last': 'Owner',
            }
        ],
        'all_members': [
            {
                'u_id': u_id2,
                'name_first': 'The',
                'name_last': 'Owner',
            },
            {
                'u_id': u_id1,
                'name_first': 'The',
                'name_last': 'User',
            }
        ],
    }


    # call detail() as authorised user and owner
    assert channel.channel_details(token2, ch_id) == correct_detail

def test_channel_details_unauthorised_user(test_environment):

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment
    channel.channel_invite(token2, ch_id, u_id1)


    # call detail() as non-authorised user
    with pytest.raises(error.AccessError):
        channel.channel_details(token3, ch_id)

def test_channel_details_invalid_user(test_environment):

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment
    channel.channel_invite(token2, ch_id, u_id1)


    # non-existent user's id
    invalid_user = token3 + 'a'
    assert channel.channel_details(invalid_user, ch_id) == {}

def test_channel_details_invalid_channel_id(test_environment):

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment
    channel.channel_invite(token2, ch_id, u_id1)

    # invalid channel id
    with pytest.raises(error.InputError):
        channel.channel_details(token1, ch_id + 1)