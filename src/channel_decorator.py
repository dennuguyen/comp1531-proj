import channels
import channel
import other
import error



# Check if token is valid
def check_token_isvalid(function):
    def inner(*args):
    # Raise AccessError if channel_id is not valid
    # Run function if token is valid
        return function(*args)
    return inner


# Check if channel_id is valid
def check_channel_id_isvalid(function):
    def inner(*args):
        token = args[0]
        channel_id = args[1]
        ch_list = channels.channels_list(token)
        isvalid = 0
        for ch in ch_list['channels']:
            if ch['channel_id'] == channel_id:
                isvalid = 1
        # Raise InputError if channel_id is not valid
        if isvalid == 0:
            raise error.InputError('channel_id is not valid')
        # Run function if channel_id is valid
        return function(*args)
    return inner


# Check if token is authorised
def check_token_isauthorised(function):
    def inner(*args):
        token = args[0]
        channel_id = args[1]
        ch_list = channels.channels_list(token)
        isauthorised = 0
        for ch in ch_list['channels']:
            if ch['channel_id'] == channel_id:
                isauthorised = 1
        # Raise AccessError if token is not authorised
        if isauthorised == 0:
            raise error.AccessError('user is not member of channel')
        # Run function if token is auhtorised
        return function(*args)
    return inner


# Check if u_id is a valid user
def check_u_id_isvalid(function):
    def inner(*args):
        token = args[0]
        u_id = args[2]
        users_list = other.users_all(token)
        isvalid = 0
        for user in users_list['users']:
            if user['u_id'] == u_id:
                isvalid = 1
    # Raise AccessError if u_id is not valid
        if isvalid == 0:
            raise error.InputError('u_id is not a valid user')
    # Run function if u_id is valid
        return function(*args)
    return inner

# Check that token is not already a member
def check_token_isnotmember(function):
    def inner(*args):
        token = args[0]
        channel_id = args[1]
        ch_list = channels.channels_list(token)
        isnotmember = 1
        for ch in ch_list['channels']:
            if ch['channel_id'] == channel_id:
                isnotmember = 0
    # Raise AccessError if u_id is a member
        if isnotmember == 1:
            raise error.AccessError('u_id is a member')
    # Run function if u_id is valid
        return function(*args)
    return inner

def check_token_ismember(function):
    def inner(*args):
        token = args[0]
        channel_id = args[1]
        ch_list = channels.channels_list(token)
        ismember = 0
        for ch in ch_list['channels']:
            if ch['channel_id'] == channel_id:
                ismember = 1
    # Raise AccessError if u_id is not a member
        if ismember == 0:
            raise error.AccessError('u_id is not a member')
    # Run function if u_id is valid
        return function(*args)
    return inner


# Check that start is equal to or greater than total number of messages in channel
def check_start_issmaller(function):
    def inner(*args):
        token = args[0]
        channel_id = args[1]
        start = args[2]
        # Raise InputError if start is equal or greater than total number of messages
        # Run function if start is smaller
        return function(*args)
    return inner

def check_token_isnotslackrking(function):
    def inner(*args):
        token = args[0]

def check_channel_isnotprivate(function):
    def inner(*args):
        