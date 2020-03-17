import channels
import channel
import other
import error



# Check if token is valid
def check_token_isvalid(function):
    def inner(token, channel_id, u_id):
    # Raise AccessError if channel_id is not valid
    # Run function if token is valid
        return function(token, channel_id, u_id)
    return inner


# Check if channel_id is valid
def check_channel_id_isvalid(function):
    def inner(token, channel_id, u_id):
        ch_list = channels.channels_list(token)
        isvalid = 0
        for ch in ch_list['channels']:
            if ch['channel_id'] == channel_id:
                isvalid = 1
        # Raise InputError if channel_id is not valid
        if isvalid == 0:
            raise error.InputError('channel_id is not valid')
        # Run function if channel_id is valid
        return function(token, channel_id, u_id)
    return inner


# Check if token is authorised
def check_token_isauthorised(function):
    def inner(token, channel_id, u_id):
        ch_details = channel.channel_details(token, channel_id)
        isauthorised = 0
        for user in ch_details['all_members']:
            if user['u_id'] == u_id:
                isauthorised = 1
        # Raise AccessError if token is not authorised
        if isauthorised == 0:
            raise error.AccessError('user is not member of channel')
        # Run function if token is auhtorised
        return function(token, channel_id, u_id)
    return inner


# Check if u_id is a valid user
def check_u_id_isvalid(function):
    def inner(token, channel_id, u_id):
        users_list = other.users_all(token)
        isvalid = 0
        for user in users_list['users']:
            if user['u_id'] == u_id:
                isvalid = 1
    # Raise AccessError if u_id is not valid
        if isvalid == 0:
            raise error.InputError('u_id is not a valid user')
    # Run function if u_id is valid
        return function(token, channel_id, u_id)
    return inner

# Check that u_id is not already a member
def check_u_id_isnotmember(function):
    def inner(token, channel_id, u_id):
        member_list = channel.channel_details(token, channel_id)
        isnotmember = 0
        for user in member_list['all_members']:
            if user['u_id'] == u_id:
                isnotmember = 1
    # Raise AccessError if u_id is not valid
        if isnotmember == 0:
            raise error.InputError('u_id is not a valid user')
    # Run function if u_id is valid
        return function(token, channel_id, u_id)
    return inner


# Check that start is equal to or greater than total number of messages in channel
def check_start_issmaller(function):
    def inner(token, channel_id, start):
        # Raise InputError if start is equal or greater than total number of messages
        # Run function if start is smaller
        return function(token, channel_id, start)
    return inner