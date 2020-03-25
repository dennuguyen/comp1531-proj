'''
Standup related functions are here
'''

from data import get_data
import authenticate as au

@au.authenticator(au.is_token_valid, au.valid_channel_id, au.already_active_standup)
def standup_start(token, channel_id, length):
    ''' Add a message to the message queue at the end of the message queue in channel.'''
    u_id = get_data().get_user_with_token(token).get_u_id()


    return {
        'time_finish' : 0
    }

@au.authenticator(au.is_token_valid, au.valid_channel_id)
def standup_active(token, channel_id):
    ''' For a given channel, return whether a standup is active in it, and what time the standup finishes. '''
    
    return {
        'is_active' : False,
        'time_finish' : 0
    }

@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_user_in_channel, au.message_length, au.already_active_standup)
def standup_send(token, channel_id, message):
    ''' Sending a message to get buffered in the standup queue, assuming a standup is currently active.'''
    
    return {}