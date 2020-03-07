import pytest
import channel
import error
import channels
import auth


@pytest.fixture(scope="module")
def test_environment(get_new_user_1, get_new_user_2):
    u_id1, token1 = get_new_user_1
    u_id2, token2 = get_new_user_2

    return u_id1, token1, u_id2, token2

# test case where owner promotes a member to owner
def test_channel_addowner_add_member(test_environment):

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment
    ch_id = channels.channels_create(token1, 'New Channel', True)
    channel.channel_join(token2, ch_id)

    # owner adds an owner
    assert channel.channel_addowner(token1, ch_id, u_id2) == {}
    assert channel.channel_details(token1, ch_id) == {
        'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'The',
                'name_last': 'Owner',
            },
            {
                'u_id': u_id2,
                'name_first': 'A',
                'name_last': 'Stranger',
            }
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': 'The',
                'name_last': 'Owner',
            },
            {
                'u_id': u_id2,
                'name_first': 'A',
                'name_last': 'Stranger',
            }
        ],
    }

# test case where owner promotes owner to owner
def test_channel_addowner_add_already_owner(test_environment):
    
    # set up environment
    u_id1, token1, u_id2, token2 = test_environment
    ch_id = channels.channels_create(token1, 'New Channel', True)
    channel.channel_join(token2, ch_id)
    channel.channel_addowner(token1, ch_id, u_id2)

    # owner promotes someone
    with pytest.raises(error.InputError):
        channel.channel_addowner(token1, ch_id, u_id2)



# test case where owner promotes stranger to owner
def test_channel_addowner_add_stranger(test_environment):

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment
    ch_id = channels.channels_create(token1, 'New Channel', True)

    # owner promotes a stranger
    assert channel.channel_addowner(token1, ch_id, u_id2) == {}
    assert channel.channel_details(token1, ch_id) == {
            'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'The',
                'name_last': 'Owner',
            },
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': 'The',
                'name_last': 'Owner',
            },
        ],
    }               


# test case where member promotes member to owner
def test_channel_addowner_unauthorised_member(test_environment, get_user_3):

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment
    u_id3, token3 = get_user_3
    ch_id = channels.channels_create(token1, 'New Channel', True)
    channel.channel_join(token2, ch_id)

    # member promotes member
    with pytest.raises(error.AccessError):
        channel.channel_addowner(token2, ch_id, u_id3)

# test case where stranger promotes member to owner
def test_channel_addowner_unauthorised_nonmember(test_environment, get_new_user_3):

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment
    u_id3, token3 = get_new_user_3
    ch_id = channels.channels_create(token1, 'New Channel', True)

    # stranger promotes member
    with pytest.raises(error.AccessError):
        channel.channel_addowner(token2, ch_id, u_id3)

# validity cases
def test_channel_addowner_invalid_channel_id(test_environment):

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment
    ch_id = channels.channels_create(token1, 'New Channel', True)

    # invalid user id
    with pytest.raises(error.InputError):
        channel.channel_addowner(token1, ch_id, u_id1 + 1)


def test_channel_addowner_invalid_u_id(test_environment):

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment
    ch_id = channels.channels_create(token1, 'New Channel', True)

    # invalid channel id

    assert channel.channel_addowner(token1, ch_id, u_id2 + 1) == {}
    assert channels.channels_list(token1) == {
            'name': 'New Channel',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'The',
                'name_last': 'Owner',
            },
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': 'The',
                'name_last': 'Owner',
            },
        ],
    }
