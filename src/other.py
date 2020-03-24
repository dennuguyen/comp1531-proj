import data

def users_all(*, token):
    '''
    Returns a list of all users and their associated details.
    '''
    user_list = [user.get_user_dict() for user in data.getData().user_list]
    return {'users' : user_list}

def search(*, token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels
    that the user has joined that match the query. Results are sorted from most
    recent message to least recent message
    '''
    # First get the user_id from the token
    u_id = data.getData().get_u_id_with_token(token)

    # Now get the list of all the channels the user has joined.
    channels_user_is_in = data.getData().get_channels_list_dict(u_id)

    # Now get a list of all messages that the query string matches
    matching_messages = []
    for channel in channels_user_is_in:
        for message_id in channel.message_id_list:
            current_message = data.getData().get_message(message_id)
            if current_message.message == query_str:
                matching_messages.append(current_message.get_message_dict())

    sorted_matching_messages = sorted(matching_messages, key=lambda message: message['time_created'])

    return {'messages' : sorted_matching_messages}
