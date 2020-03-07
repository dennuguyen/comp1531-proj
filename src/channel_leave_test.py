import pytest
import channel
import error
import channels
import auth

def test_environment():
    u_id1, token1 = auth_register('example@unsw.com', 'password', 'The', 'Owner')
    u_id2, token2 = auth_register('owner@unsw.com', 'password', 'The', 'User')
    u_id3, token3 = auth_register('stranger@unsw.com', 'password', 'A', 'Stranger')
    
    return u_id1, token1, u_id2, token2, u_id3, token3

# case where user leaves
def test_channel_leave_user_leaves():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()
    ch_id = channels.channels_create(token1, 'New Channel', True) # u_id1 is owner
    channel.channel_join(token2, ch_id)

    # user leaves
    assert channel.channel_leave(token2, ch_id) == {}
    assert channels.channels_list(token2)['channels'] == [] 

# case where channel is owner leaves and user is promoted for channel populated by two
def test_channel_leave_owner_leaves():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()
    ch_id = channels.channels_create(token1, 'New Channel', True) # u_id1 is owner
    channel.channel_join(token2, ch_id)

    # owner leaves
    assert channel.channel_leave(token1, ch_id) == {}
    assert channel.channel_list(token1)['channels'] == []
    assert channel.channel_details(token2) == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': ch_id,
                'name_first': 'The',
                'name_last': 'User',
            }
        ],
        'all_members': [
            {
                'u_id': ch_id,
                'name_first': 'The',
                'name_last': 'User',
            }
        ],
    }

# case where channel is populated by a sole owner
def test_channel_leave_3():

    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()
    ch_id = channels.channels_create(token1, 'New Channel', True) # u_id1 is owner

    # owner leaves
    assert channel.channel_leave(token1, ch_id) == {}
    assert channel.channel_list(token1)['channels'] == []
    assert channel.channel_details(token1) == {
        'name': 'New Channel',
        'owner_members': [
            {

            }
        ],
        'all_members': [
            {

            }
        ],
    }

# invalid id and token cases
def test_channel_leave_invalid_channel_id():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()
    ch_id = channels.channels_create(token1, 'New Channel', True) # u_id1 is owner
    channel.channel_join(token2, ch_id)

    # invalid channel id
    with pytest.raises(error.InputError)
        channel_leave(token2, ch_id + 1)


def test_channel_leave_unauthorised_user():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail = test_environment()
    ch_id = channels.channels_create(token1, 'New Channel', True) # u_id1 is owner
    channel.channel_join(token2, ch_id)

    # invalid token
    with pytest.raises(error.AccessError)
        channel_leave(token3, ch_id) # equivalent to stranger leaving channel
