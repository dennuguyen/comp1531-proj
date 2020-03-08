import pytest
import channel
import error
import channels
import auth

def test_environment():
    u_id1, token1 = auth_register('owner@unsw.com', 'password', 'The', 'Owner')
    u_id2, token2 = auth_register('stranger@unsw.com', 'password', 'A', 'Stranger')


    return u_id1, token1, u_id2, token2

def test_channel_join_public():

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment()
    ch_id = channels.channels_create(token1, 'Test channel1', True)['channel_id']

    # stranger joins public channel
    assert channel.channel_join(token2, ch_id) == {}
    assert channels.channels_details(token2, ch_id) == {
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

def test_channel_join_private():

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment()
    ch_id = channels.channels_create(token1, 'Test channel1', False)['channel_id']

    # stranger joins private channel
    with pytest.raises(error.AccessError):
        channel.channel_join(token2, ch_id)

def test_channel_join_invalid_channel():

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment()
    ch_id = channels.channels_create(token1, 'Test channel1', False)['channel_id']

    # stranger joins private channel
    with pytest.raises(error.InputError):
        channel.channel_join(token2, ch_id+1)


def test_channel_join_already_member():

    # set up environment
    u_id1, token1, u_id2, token2 = test_environment()
    ch_id1 = channels.channels_create(token1, 'Test channel1', True)['channel_id']
    channel.channel_join(token2, ch_id1)

    ch_id2 = channels.channels_create(token1, 'Test channel2', False)['channel_id']
    channel.channel_join(token2, ch_id2)

    assert channel.channel_join(token1, ch_id1) == {}
    assert channel.channel_join(token2, ch_id1) == {}
    assert channel.channel_join(token1, ch_id2) == {}
    assert channel.channel_join(token2, ch_id2) == {}