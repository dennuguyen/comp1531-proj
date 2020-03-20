###### Raymonds Decorators #######
import channels
import channel
import other
import error



# Check if token is valid
def check_token_isvalid(function):
    def inner(**kwargs):
    # Raise AccessError if channel_id is not valid
    # Run function if token is valid
        return function(**kwargs)
    return inner


# Check if channel_id is valid
def check_channel_id_isvalid(function):
    def inner(**kwargs):
        token = kwargs['token']
        channel_id = kwargs['channel_id']
        ch_list = channels.channels_list(token)
        isvalid = 0
        for ch in ch_list['channels']:
            if ch['channel_id'] == channel_id:
                isvalid = 1
        # Raise InputError if channel_id is not valid
        if isvalid == 0:
            raise error.InputError('channel_id is not valid')
        # Run function if channel_id is valid
        return function(**kwargs)
    return inner


# Check if token is authorised
def check_token_isauthorised(function):
    def inner(**kwargs):
        token = kwargs['token']
        channel_id = kwargs['channel_id']
        ch_list = channels.channels_list(token)
        isauthorised = 0
        for ch in ch_list['channels']:
            if ch['channel_id'] == channel_id:
                isauthorised = 1
        # Raise AccessError if token is not authorised
        if isauthorised == 0:
            raise error.AccessError('user is not member of channel')
        # Run function if token is auhtorised
        return function(**kwargs)
    return inner


# Check if u_id is a valid user
def check_u_id_isvalid(function):
    def inner(**kwargs):
        token = kwargs['token']
        u_id = kwargs['u_id']
        users_list = other.users_all(token)
        isvalid = 0
        for user in users_list['users']:
            if user['u_id'] == u_id:
                isvalid = 1
    # Raise AccessError if u_id is not valid
        if isvalid == 0:
            raise error.InputError('u_id is not a valid user')
    # Run function if u_id is valid
        return function(**kwargs)
    return inner

# Check that token is not already a member
def check_token_isnotmember(function):
    def inner(**kwargs):
        token = kwargs['token']
        channel_id = kwargs['channel_id']
        ch_list = channels.channels_list(token)
        isnotmember = 1
        for ch in ch_list['channels']:
            if ch['channel_id'] == channel_id:
                isnotmember = 0
    # Raise AccessError if u_id is a member
        if isnotmember == 1:
            raise error.AccessError('u_id is a member')
    # Run function if u_id is valid
        return function(**kwargs)
    return inner

# Check that start is equal to or greater than total number of messages in channel
def check_start_issmaller(function):
    def inner(**kwargs):
        token = kwargs['token']
        channel_id = kwargs['channel_id']
        start = kwargs['start']
        # Raise InputError if start is equal or greater than total number of messages
        # Run function if start is smaller
        return function(**kwargs)
    return inner

def check_token_isnotslackrking(function):
    def inner(**kwargs):
        token = kwargs['token']

def check_token_ismember(function):
    def inner(**kwargs):
        token = kwargs['token']
        channel_id = kwargs['channel_id']
        ch_list = channels.channels_list(token)
        ismember = 0
        for ch in ch_list['channels']:
            if ch['channel_id'] == channel_id:
                ismember = 1
    # Raise AccessError if u_id is not a member
        if ismember == 0:
            raise error.AccessError('u_id is not a member')
    # Run function if u_id is valid
        return function(**kwargs)
    return inner

def check_channel_isnotprivate(function):
    def inner(**kwargs):
        return function(**kwargs)
    return inner

def check_token_isowner(function):
    def inner(**kwargs):
        token = kwargs['token']
        channel_id = kwargs['channel_id']
        ch_details = channel.channel_details(token, channel_id)
        return function(**kwargs)
    return inner

def check_u_id_isnotowner(function):
    pass

def check_u_id_isowner(function):
    pass

############


import re
import error
import user
import data
import auth_helper


def authenticate_token(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the token
        token = kwargs['token']

        # Assert the token
        # assert token == 1

        return fn(*args, **kwargs)

    return wrapper


def authenticate_u_id(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the u_id
        u_id = kwargs['u_id']
        print(u_id)

        return fn(*args, **kwargs)

    return wrapper


def authenticate_email(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # Check the email form
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(regex, email):
            raise error.InputError('Invalid email.')
        else:
            pass

        return fn(*args, **kwargs)

    return wrapper


def register_email(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # Check if email already exists
        for registered_user in data.data['users']:
            if email == registered_user['email']:
                raise error.InputError('Email already exists.')
            else:
                pass

        return fn(*args, **kwargs)

    return wrapper


def authenticate_password(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the password
        email = kwargs['email']
        password = kwargs['password']

        # Retrieve the salt by looking up the email in the passwords dictionary
        for i in range(len(data.data['passwords'])):
            if email == data.data['passwords'][i].get('email'):

                # Get the salt from passwords dictionary
                salt = data.data['passwords'][i]['salt']

                # Get the hash for salt + password combination
                try_hash = auth_helper.get_hash(salt, password)

                # Try the hash. If incorrect raise InputError
                if try_hash != data.data['passwords'][i]['hash']:
                    raise error.InputError

                break  # No need to continue

        return fn(*args, **kwargs)

    return wrapper


def authenticate_name_first(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the first name
        name_first = kwargs['name_first']
        print(name_first)

        return fn(*args, **kwargs)

    return wrapper


def authenticate_name_last(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the password
        name_last = kwargs['name_last']
        print(name_last)

        return fn(*args, **kwargs)

    return wrapper


def authenticate_handle_str(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the password
        handle_str = kwargs['handle_str']
        print(handle_str)

        return fn(*args, **kwargs)

    return wrapper