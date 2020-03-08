import pytest
import channel
import error
import channels
import auth

def test_environment():
    u_id1, token1 = auth.auth_register('example@unsw.com', 'password', 'The', 'Owner')
    u_id2, token2 = auth.auth_register('user@unsw.com', 'password', 'The', 'User')
    u_id3, token3 = auth.auth_register('stranger@unsw.com', 'password', 'A', 'Stranger')
    ch_id = channels.channels_create(token1, 'New Channel', True) # u_id1 is owner

    return u_id1, token1, u_id2, token2, u_id3, token3, ch_id

# test case where an owner removes another owner
def test_channel_removeowner_owner_remove_owner():

    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
    channel.channel_join(token2, ch_id)
    channel.channel_addowner(token1, ch_id, u_id2) # promote user 2 to owner

    # owner 1 removes owner 2
    assert channel.channel_removeowner(token1, ch_id, u_id2) == {}
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
            {
                'u_id': u_id2,
                'name_first': 'The',
                'name_last': 'User',
            }
        ],
    }


############### COMPLETE TEST FUNCTIONS BELOW #####################

# test case where owner tries to remove themself
def test_channel_removeowner_owner_remove_themself():
    
    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
    channel.channel_join(token2, ch_id)
    channel.channel_addowner(token1, ch_id, u_id2)  

    #Actual test
    assert channel.channel_removeowner(token1, ch_id, u_id1) == {}  
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
            {
                'u_id': u_id2,
                'name_first': 'The',
                'name_last': 'User',
            }
        ]
    }

def test_channel_removeowner_owner_slackr_remove_owner():

    u_id1, token1 = auth.auth_register('example@unsw.com', 'password', 'The', 'Owner')
    u_id2, token2 = auth.auth_register('user@unsw.com', 'password', 'The', 'User')
    u_id3, token3 = auth.auth_register('stranger@unsw.com', 'password', 'A', 'Stranger')
    ch_id = channels.channels_create(token2, 'New Channel', True) # u_id2 is owner

    assert channel.channel_removeowner(token1, ch_id, u_id2) == {}
    assert channel.channel_details(token1, ch_id) == {
            'name': 'New Channel',
        'owner_members': [

        ],
        'all_members': [

        ]
    }


# test case where sole owner tries to remove themself
def test_channel_removeowner_owner_remove_themself_only_member():
    
    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
 

    #Actual test
    assert channel.channel_removeowner(token1, ch_id, u_id1) == {}  
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
            }
        ],
    }

# test case where member tries to remove owner
def test_channel_removeowner_unauthorised_user_id():
    
    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
    channel.channel_join(token2, ch_id)
 
    with pytest.raises(InputError):
        channel.channel_removeowner(token2, ch_id, u_id1)

def test_channel_removeowner_invalid_channel_id():
    
    # set up environment
    u_id1, token1, u_id2, token2, u_id3, token3, ch_id = test_environment()
    channel.channel_join(token2, ch_id)
    channel.channel_addowner(token1, ch_id, u_id2)
 
    with pytest.raises(error.InputError):
        channel.channel_removeowner(token1, ch_id+1, u_id2)