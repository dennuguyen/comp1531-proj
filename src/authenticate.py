###### Raymonds Decorators #######
import channels
import channel
import other
import error
import re



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



######################## Input Errors #######################3



def valid_email(fn):
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # Check the email form
        valid_email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(valid_email_regex, email):
            raise error.InputError('Invalid email.')

        return fn(*args, **kwargs)

    return wrapper


def existing_email(fn):
    '''
    Checks the email actually exists (For Login)
    '''
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # Check if email doesn't exist
        email_existance = False
        for registered_user in data.data['users']: # TODO: Check data structure when finalised
            if email == registered_user['email']:
                email_existance = True

        # If it doesn't exist, raise an error
        if not email_existance:
            raise error.InputError("This email does not exist")

        return fn(*args, **kwargs)

    return wrapper



def authenticate_password(fn):
    def wrapper(*args, **kwargs):

        # Get the email and password
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

def email_already_used(fn):
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # Check if email already exists
        for registered_user in data.data['users']: # TODO: Check data structure when finalised
            if email == registered_user['email']:
                raise error.InputError('Email already exists.')

        return fn(*args, **kwargs)

    return wrapper

def check_password_length(fn):
    def wrapper(*args, **kwargs):

        # Get the password
        password = kwargs['password']

        if len(password) < 6:
            raise error.InputError('Password is too short. Must be longer than 6 characters')

        return fn(*args, **kwargs)

    return wrapper

def check_name_length(fn):
    def wrapper(*args, **kwargs):

        # Get first and last name
        first_name, last_name = kwargs['name_first'], kwargs['name_last']

        # Is first and name between 1 and 50 characters inclusive?
        check_first_length = 1 <= len(first_name) <= 50
        check_last_length = 1 <= len(last_name) <= 50

        if not (check_first_length and check_last_length):
            raise error.InputError('First and last name must be between 1 and 50 characters inclusive.')

        return fn(*args, **kwargs)

    return wrapper

def is_user_in_channel(fn):
    def wrapper(*args, **kwargs):
        '''
        channel_id does not refer to a valid channel that the authorised user is part of.
        '''
        # Get the channel id and user id in reference
        channel_id, u_id = kwargs['channel_id'], kwargs['u_id']

        # Find the channel respective to the u_id
        channel_with_id = {}
        for channel in data.data['channels']: # TODO Check valid data use
            if channel_id == channel['channel_id']:
                channel_with_id = channel
                break
        
        # Now we either have a channel or not. If its empty, invalid. Else we need to check if user is in it
        if not channel_with_id:
            raise error.InputError('The channel does not exist.')

        # Now we are in a situation where we have an actual channel. Now to check if user is in it.
        user_in_channel = False
        for user in channel_with_id['all_members']:
            if u_id = user['u_id']:
                user_in_channel = True
                break

        # If user is not in the channel. Input error
        if not user_in_channel:
            raise error.InputError('The user is not in this channel.')

        return fn(*args, **kwargs)
    
    return wrapper

def check_u_id_existance(fn):
    '''
    u_id does not refer to a valid user
    '''
    def wrapper(*args, **kwargs):
        # Get user id
        u_id = kwargs['u_id']

        # Assume the user does not exist
        user_exists = False
        for user in data.data['users']:
            if u_id = user['u_id']:
                user_exists = True
                break
        
        if not user_exists:
            raise error.InputError('u_id does not refer to a valid user')

        return fn(*args, **kwargs)

    return wrapper

def valid_channel_id(fn):
    '''
    Channel ID is not a valid channel
    TODO: This has repeated code with is_user_in_channel. Fix
    '''
    def wrapper(*args, **kwargs):

        # Get channel id
        channel_id = kwargs['channel_id']

        # Assume channel does not exist
        channel_exists = False
        for channel in data.data['channels']: # TODO Check valid data use
            if channel_id == channel['channel_id']:
                channel_exists = True
                break
        
        # Now we either have a channel or not. If its empty, invalid. Else we need to check if user is in it
        if not channel_exists:
            raise error.InputError('Channel ID is not a valid channel.')

        return fn(*args, **kwargs)

    return wrapper

def start_has_more_messages(fn):
    '''
    start is greater than or equal to the total number of messages in the channel
    '''

    def wrapper(*args, **kwargs):

        # Get start number
        start = kwargs['start']
        channel_id = kwargs['channel_id']

        # Get the channel with the id in question. TODO: If there is no channel... fail!
        channel_with_id = {}
        for channel in data.data['channels']: # TODO Check valid data use
            if channel_id == channel['channel_id']:
                channel_with_id = channel
                break
                
        if start > len(channel_with_id['messages']):
            raise error.InputError('Start is greater than or equal to the total number of messages in the channel.')

        return fn(*args, **kwargs)
    
    return wrapper


def already_owner(fn):
    '''
    When user with user id u_id is already an owner of the channel
    '''

    def wrapper(*args, **kwargs):

        # Get user and channel id
        u_id, channel_id = kwargs['u_id'], kwargs['channel_id']

        # Get the channel with the id in question. TODO: If there is no channel... fail!
        channel_with_id = {}
        for channel in data.data['channels']: # TODO Check valid data use
            if channel_id == channel['channel_id']:
                channel_with_id = channel
                break

        if channel_with_id['owner_members']['u_id'] == u_id: # TODO Check if there can be multiple owners?!?!
            raise error.InputError('When user with user id u_id is already an owner of the channel')

        return fn(*args, **kwargs)

    return wrapper

def not_owner(fn):
    '''
    When user with user id u_id is not an owner of the channel
    '''

    def wrapper(*args, **kwargs):

        # Get user and channel id
        u_id, channel_id = kwargs['u_id'], kwargs['channel_id']

        # Get the channel with the id in question. TODO: If there is no channel... fail!
        channel_with_id = {}
        for channel in data.data['channels']: # TODO Check valid data use
            if channel_id == channel['channel_id']:
                channel_with_id = channel
                break

        if channel_with_id['owner_members']['u_id'] != u_id:
            raise error.InputError('When user with user id u_id is not an owner of the channel')

        return fn(*args, **kwargs)

    return wrapper

def channel_name_length(fn):
    '''
    Name is more than 20 characters long
    '''
    def wrapper(*args, **kwargs):

        # Get channel name
        channel_name = kwargs['name']

        if len(channel_name) > 20:
            raise error.InputError('Name is more than 20 characters long')

        return fn(*args, **kwargs)

    return wrapper

def message_length(fn):
    '''
    Message is more than 1000 characters
    '''
    def wrapper(*args, **kwargs):

        # Get message
        message = kwargs['message']

        if len(message) > 1000:
            raise error.InputError('Message is more than 1000 characters.')

        return fn(*args, **kwargs)

    return wrapper

def send_message_in_future(fn):
    '''
    Time sent is a time in the past
    '''

    def wrapper(*args, **kwargs):
        from datetime import datetime
        # Get time TODO: Check what object this time is in?
        time = datetime([kwargs['time']])

        if time < datetime.now():
            raise error.InputError('Time sent is a time in the past')

        return fn(*args, **kwargs)
    
    return wrapper

def is_message_id_in_channel(fn):

    '''
    message_id is not a valid message within a channel that the authorised user has joined
    '''

    def wrapper(*args, **kwargs):

        # Get message id and channel_id
        message_id = kwargs['message_id']
        channel_id = kwargs['channel_id']

        #TODO ### WHAT ###
        # how can I check the channel or any of that. I'm only given a token, message_id and react_id. No channel_id?

def is_valid_react_id(fn):
    '''
    react_id is not a valid React ID. The only valid react ID the frontend has is 1
    '''
    def wrapper(*args, **kwargs):

        react_id = kwargs['react_id']

        if react_id != 1:
            raise error.InputError('react_id is not a valid React ID. The only valid react ID is 1')

        return fn(*args, **kwargs)

    return wrapper

def already_contains_react(fn):
    pass
    # TODO ### WHAT ###
     # how can I check the channel or any of that. I'm only given a token, message_id and react_id. No channel_id?