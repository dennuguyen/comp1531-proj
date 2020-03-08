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

def test_channel_join_public(test_environment):

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment
    ch_id = channels.channels_create(token1, 'Test channel1', True)['channel_id']

    # stranger joins public channel
    assert channel.channel_join(token2, ch_id) == {}
    assert channel.channel_details(token2, ch_id) == {
        'name': 'Test channel1',
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': 'The',
                'name_last': 'Owner',
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

def test_channel_join_private(test_environment):

    # set up environment
    _, token1, _, token2 = test_environment
    ch_id = channels.channels_create(token1, 'Test channel1', False)['channel_id']

    # stranger joins private channel
    with pytest.raises(error.AccessError):
        channel.channel_join(token2, ch_id)

def test_channel_join_invalid_channel(test_environment):

    # set up environment
    _, token1, _, token2 = test_environment
    ch_id = channels.channels_create(token1, 'Test channel1', False)['channel_id']

    # stranger joins private channel
    with pytest.raises(error.InputError):
        channel.channel_join(token2, ch_id+1)


def test_channel_join_already_member(test_environment):

    # set up environment
    _, token1, _, token2 = test_environment
    ch_id1 = channels.channels_create(token1, 'Test channel1', True)['channel_id']
    channel.channel_join(token2, ch_id1)

    ch_id2 = channels.channels_create(token1, 'Test channel2', False)['channel_id']
    channel.channel_join(token2, ch_id2)

    assert channel.channel_join(token1, ch_id1) == {}
    assert channel.channel_join(token2, ch_id1) == {}
    assert channel.channel_join(token1, ch_id2) == {}
    assert channel.channel_join(token2, ch_id2) == {}