def channel_invite(token, channel_id, u_id):

# Check if token is valid
    # Raise AccessError if token is not valid

# Check if channel_id is valid
    # Raise InputError if channel_id is not valid

# Check if token is part of channel
    # Raise InputError if token is not part of channel

# Check if u_id is valid
    # Raise InputError if u_id is not a valid u_id

# Check if u_id is already a member
    # Raise AccessError if u_id is already a member

# If all conditions are met add u_id to channel as member
    # Edit relevant databases

# Return {}

    return {
    }


def channel_details(token, channel_id):

# Check that token is valid
    # Raise AccessError if token is not valid

# Check channel_id is valid
    # Raise InputError if channel_id is not valid

# Check token is member of channel
    # Raise AccessError if token is not member of channel

# If all conditions are met 
    # Return {name, owner_members, all_members}

    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }


def channel_messages(token, channel_id, start):

# Check token is valid
    # Raise AccessError if token is not valid

# Check channel_id is valid
    # Raise InputError if channel_id is not valid

# Check token is a member of channel
    # Raise AccessError if token is not a member of channel

# Check that start is equal to or greater than total number of messages in channel
    # Raise InputError if start is euqal or greater than total number of messages

# If all conditions are met
    # If end is less than total messages
        # Return {messages, start, end}
    # Else if end is greater than total messages
        # Return {messages, start, -1}

    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }


def channel_leave(token, channel_id):


    return {
    }


def channel_join(token, channel_id):
    return {
    }


def channel_addowner(token, channel_id, u_id):
    return {
    }


def channel_removeowner(token, channel_id, u_id):
    return {
    }
