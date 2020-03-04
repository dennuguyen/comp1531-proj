#Raymond: Message.py helper functions

import pytest
import message
import auth
import channels

@pytest.fixture
def get_new_user1():
    email = 'z1111111@unsw.com'
    password = 'qwert111'
    name_first = 'James'
    name_last = 'Bond'
    register_retval = auth.auth_register(email, password, name_first, name_last)
    return(register_retval['u_id'], register_retval['token'])

def get_new_channel(get_new_user1):
    token = get_new_user1[1]
    channel_name = 'Test Channel1'    
    is_public = True(
    channel_id = channels.channels_create(token, channel_name, is_public )
    return )channel_id)

