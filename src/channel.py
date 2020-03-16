def channel_invite(token, channel_id, u_id):

# Check if token is valid
    # Raise AccessError if token is not valid

# Check if channel_id is valid
channels = channels_listall(token)
ch_valid = False
for x['channel_id'] in channels['channels']:
    if channel_id = x['channel_id']:
        ch_valid = True
    # Raise InputError if channel_id is not valid
if ch_valid == False:
    raise InputError('channel_id is not valid')

# Check if token is part of channel
channel_details = channel_details(token, channel_id)
token_authorised = False
for x['u_id'] in channel_details['all_members']:
    if u_id = x['u_id']:
        token_authorised = True
    # Raise InputError if token is not part of channel
if token_authorised == False:
    raise InputError('user is not member of channel')
    
# Check if u_id is valid



    # Raise InputError if u_id is not a valid u_id

# Check if u_id is already a member
    # Raise AccessError if u_id is already a member

# If all conditions are met add u_id to channel as member
    # Edit relevant databases

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
