'''
The other.py file has two main functions.

users_all(.) - returns the details of everyone that's signed up to slackr.

search(.) - Searches for a specific string
'''

import data
import authenticate as au

@au.authenticator(au.is_token_valid)
def users_all(*, token):
    '''
    Returns a list of all users and their associated details.
    '''
    # Get a list of all User classes.
    users = data.get_data().get_user_list()

    # Convert this into a list of required dictionaries
    user_list = [user.get_user_dict() for user in users]

    return {'users' : user_list}

@au.authenticator(au.is_token_valid)
def search(*, token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels
    that the user has joined that match the query. Results are sorted from most
    recent message to least recent message
    '''
    # First get the user_id from the token
    u_id = data.get_data().get_user_with_token(token)

    # Get a list of all the Channel classes.
    channels = data.get_data().get_channel_list()

    # Now get an object which contains all the channels which the user has joined
    channels_user_is_in = filter(lambda channel: u_id in channel.get_u_id_list(), channels)

    # Now get a list of all Message classes if they match the query string.
    # TODO: Get a second opiniion on this absolute garbage.
    matching_messages = []
    for channel in channels_user_is_in:
        for message_id in channel.get_msg_id_list():
            current_message = data.get_data().get_message_with_message_id(message_id)
            if query_str == current_message.get_message():
                matching_messages.append(current_message.get_message_dict())

    sorted_messages = sorted(matching_messages, key=lambda message: message['time_created'])

    return {'messages' : sorted_messages}
