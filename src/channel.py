
from channel_decorator import check_token_isvalid
from channel_decorator import check_channel_id_isvalid
from channel_decorator import check_token_isauthorised
from channel_decorator import check_u_id_isvalid
from channel_decorator import check_u_id_isnotmember
from channel_decorator import check_start_issmaller

@check_token_isvalid
@check_channel_id_isvalid
@check_token_isauthorised
@check_u_id_isvalid
@check_u_id_isnotmember
def channel_invite(token, channel_id, u_id):

# If all conditions are met add u_id to channel as member
    # Edit relevant databases

    return {
    }

@check_token_isvalid
@check_channel_id_isvalid
@check_token_isauthorised
def channel_details(token, channel_id):

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

@check_token_isvalid
@check_channel_id_isvalid
@check_token_isauthorised
@check_start_issmaller
def channel_messages(token, channel_id, start):

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

# Check token is valid
    # Raise AccessError if token is not valid

# Check channel_id is valid
    # Raise InputError if channel_id is not valid

# Check token is a member of channel
    # Raise AccessError if token is not a member of channel

# If all conditions are met
    # Remove user from channel member list

    return {
    }


def channel_join(token, channel_id):

# Check token is valid
    # Raise AccessError if token is not valid

# Check channel_id is valid
    # Raise InputError if channel_id is not valid

# Check channel is not private
    # Raise AccessError if channel is private

# If all conditons are met
    # Add token to channel member list

    return {
    }


def channel_addowner(token, channel_id, u_id):

# Check token is valid
    # Raise AccessError if token is not valid

# Check token is authorised
    # Raise AccessError if token is not authorised

# Check channel_id is valid
    # Raise InputError if channel_id is not valid

# Check u_id is not already an owner
    # Raise InputError if u_id is already an owner of the channel

# If all conditons are met
    # Add u_id into channel owner list

    return {
    }


def channel_removeowner(token, channel_id, u_id):

# Check token is valid
    # Raise AccessError if token is not valid

# Check token is authorised
    # Raise AccessError if token is not authorised

# Check channel_id is valid
    # Raise InputError if channel_id is not valid

# Check u_id is an owner
    # Raise InputError if u_id is not an owner of the channel

# If all conditons are met
    # Remove u_id from channel owner list

    return {
    }
