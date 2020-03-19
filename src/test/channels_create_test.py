import pytest
import channels
import channel
import error
import sys
sys.path.append('../')


# Create a public channel
def test_channels_create_public(get_new_user_1, get_channel_name_1):

    # Get user 1 and create a public channel
    token1 = get_new_user_1[1]
    ch_id1 = channels.channels_create(
        token1, get_channel_name_1, True)['channel_id']

    # Search for a single channel created in channels_listall
    flag = 0
    for channel in channels.channels_listall(token1)['channels']:
        if channel['channel_id'] == ch_id1:
            flag += 1

    assert flag == 1


# Create a private channel
def test_channels_create_private(get_new_user_1, get_channel_name_1):

    # Get user 1 and create a private channel
    token1 = get_new_user_1[1]
    ch_id1 = channels.channels_create(
        token1, get_channel_name_1, False)['channel_id']

    # Search for a single channel created in channels_listall
    flag = 0
    for channel in channels.channels_listall(token1)['channels']:
        if channel['channel_id'] == ch_id1:
            flag += 1

    assert flag == 1


# Create multiple channels
def test_channels_create_multiple(get_new_user_1, get_channel_name_1, get_channel_name_2):

    # Get user 1 and create some channels
    token1 = get_new_user_1[1]
    ch_id1 = channels.channels_create(
        token1, get_channel_name_1, False)['channel_id']
    ch_id2 = channels.channels_create(
        token1, get_channel_name_1, False)['channel_id']
    ch_id3 = channels.channels_create(
        token1, get_channel_name_2, False)['channel_id']

    # Search for three channels created in channels_listall
    flag = 0
    for channel in channels.channels_listall(token1)['channels']:
        if channel['channel_id'] == ch_id1 or channel['channel_id'] == ch_id2 or channel['channel_id'] == ch_id3:
            flag += 1

    assert flag == 3


# Create a channel with an invalid token
def test_channels_create_invalid_token(get_new_user_1, get_channel_name_1):

    # Get user 1 and an invalid token
    token1 = get_new_user_1[1]
    invalid_token = token1 + 'a'

    # Test
    with pytest.raises(error.AccessError):
        channels.channels_create(invalid_token, get_channel_name_1, True)


# Test case for creating a channel with invalid name
def test_channels_create_invalid_name(get_new_user_1):

    # Get user 1
    token1 = get_new_user_1[1]

    # Channel name cannot be empty
    with pytest.raises(error.InputError):
        channels.channels_create(token1, '', False)

    # Channel name cannot consist of only whitespace
    with pytest.raises(error.InputError):
        channels.channels_create(token1, '   ', False)

    # Channel name > 20 char
    with pytest.raises(error.InputError):
        channels.channels_create(token1, '0123456789 0123456789', True)


# Creator of the channel is the owner of the channel
def test_channels_create_channel_owner(get_new_user_1, get_new_user_detail_1, get_channel_name_1):

    # Get user 1 and some channels
    u_id1, token1 = get_new_user_1
    _, _, name_first1, name_last1 = get_new_user_detail_1
    ch_id1 = channels.channels_create(
        token1, get_channel_name_1, True)['channel_id']

    # Check if user 1 is owner of channel
    assert channel.channel_details(token1, ch_id1) == {
        'name':
        get_channel_name_1,
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': name_first1,
                'name_last': name_last1,
            },
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': name_first1,
                'name_last': name_last1,
            },
        ],
    }


# Slackr owner is automatically joins created channels (public & private)
def test_channels_create_slackr_owner(get_new_user_1, get_new_user_detail_1, get_new_user_2, get_new_user_detail_2, get_channel_name_1):

    # Get user 1
    u_id1, token1 = get_new_user_1
    _, _, name_first1, name_last1 = get_new_user_detail_1
    assert u_id1 == 1  # slackr owner user id

    # Get user 2
    u_id2, token2 = get_new_user_2
    _, _, name_first2, name_last2 = get_new_user_detail_2

    # Create a public channel
    ch_id1 = channels.channels_create(
        token2, get_channel_name_1, True)['channel_id']

    # Check if user 1 is owner of channel
    assert channel.channel_details(token1, ch_id1) == {
        'name':
        get_channel_name_1,
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': name_first1,
                'name_last': name_last1,
            },
            {
                'u_id': u_id2,
                'name_first': name_first2,
                'name_last': name_last2,
            },
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': name_first1,
                'name_last': name_last1,
            },
            {
                'u_id': u_id2,
                'name_first': name_first2,
                'name_last': name_last2,
            },
        ],
    }

    # Create a private channel
    ch_id2 = channels.channels_create(
        token2, get_channel_name_1, False)['channel_id']

    # Check if user 1 is owner of channel
    assert channel.channel_details(token1, ch_id2) == {
        'name':
        get_channel_name_1,
        'owner_members': [
            {
                'u_id': u_id1,
                'name_first': name_first1,
                'name_last': name_last1,
            },
            {
                'u_id': u_id2,
                'name_first': name_first2,
                'name_last': name_last2,
            },
        ],
        'all_members': [
            {
                'u_id': u_id1,
                'name_first': name_first1,
                'name_last': name_last1,
            },
            {
                'u_id': u_id2,
                'name_first': name_first2,
                'name_last': name_last2,
            },
        ],
    }
