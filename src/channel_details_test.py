import pytest
from channel import channel_details, channel_invite
from error import *
from channels import channels_create
from auth import auth_register

@pytest.fixture(scope="module")
def test_environment(get_new_user_1, get_new_user_2, get_new_user_3):

    u_id1, token1 = get_new_user_3
    u_id2, token2 = get_new_user_1
    u_id3, token3 = get_new_user_2
    ch_id = channels_create(token2, 'New Channel', True) # u_id2 is owner

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
                'u_id': u_id1,
                'name_first': 'The',
                'name_last': 'User',
            }
        ],
    }

    return u_id1, token1, u_id2, token2, u_id3, token3, ch_id, correct_detail

def test_channel_details(test_environment):

    # set up environment
    u_id1, token1, _, token2, _, token3, ch_id, correct_detail = test_environment
    channel_invite(token2, ch_id, u_id1) # owner invites u_id1

    # call detail() as authorised user and owner
    assert channel_details(token1, ch_id) == correct_detail
    assert channel_details(token2, ch_id) == correct_detail

    # call detail() as non-authorised user
    with pytest.raises(AccessError):
        channel_details(token3, ch_id)

    # non-existent user's id
    with pytest.raises(AccessError):
        channel_details(token1 + token2 + token3, ch_id)

    # invalid channel id
    with pytest.raises(InputError):
        channel_details(token1, ch_id + 1)
