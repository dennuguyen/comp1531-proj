'''
This file is composed of many decorator functions aimed to check specific "Input Error" cases and "Access Error" cases.

If the function you are writing for has an Input or Access error condition, for example "Email entered does not belong to a user".
Control + F to search for the function required to test for it then follow the example below.



EXAMPLES ON USE:

The use of this ultimate decorator is quite simple.
I will show an example on how to check for all input errors in the first function: "auth/login"

from authenticate import *

@authenticator(valid_email, email_does_not_exist, authenticate_password)
def login():
    pass

If we don't want to use the * import method. I will show an example for the first function "auth/login"

import authenticate

@authenticate.authenticator(authenticate.valid_email, authenticate.email_does_not_exist, authenticate.authenticate_password)
def login():
    pass

'''


import re
import error
import user
import data
import auth_helper
import time

import data

######################## Access Errors ########################

def is_token_valid(fn):
    '''
    token passed in is not a valid token
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']

        # Get a list of all those who are logged in
        logged_in_list = data.get_data().get_login_list()

        # Get a map variable of all valid tokens.
        valid_tokens = map(lambda logged_in_user: logged_in_user.get_token(), logged_in_list)

        # If the token is not in the list (technically mapping) of valid tokens. Raise Error.
        if not token in valid_tokens:
            raise error.AccessError('token passed in is not a valid token')
    
        # Else, return the function.
        return fn(*args, **kwargs)
    
    return wrapper

def is_not_member(fn):
    '''
    Authorised user is not a member of channel with channel_id.

    the authorised user has not joined the channel they are trying to post to.

    the authorised user is not already a member of the channel
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']
        channel_id = kwargs['channel_id']

        # Get the corresponding user with the token.
        user_id = data.get_data().get_user_with_token(token)

        # Get corresponding channel with the channel_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Check if user is in the channel. If not, raise an error.
        if not user_id in channel_with_id.get_u_id_list():
            raise error.AccessError(f'user is not a member of channel with {channel_id}.')

        # Else, return the function
        return fn(*args, **kwargs)

    return wrapper

def is_private_not_admin(fn):
    '''
    channel_id refers to a channel that is private (when the authorised user is not an admin)

    TODO: Unable to complete since I don't know the definition of admin.
    '''
    def wrapper(*args, **kwargs):
        channel_id = kwargs['channel_id']
        token = kwargs['token']

        # Get User class with token
        user = data.get_data().get_user_with_token(token)

        # Get Channel class with channel_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Check if user is admin TODO: Complete this
        is_admin = False # False by default.

        # If the user is not an admin. We check if the channel is private.
        # If private, raise an error
        if not is_admin:
            if channel_with_id.get_is_private():
                raise error.AccessError('channel_id refers to a channel that is private (when the authorised user is not an admin)')

        return fn(*args, **kwargs)

    return wrapper


def not_ch_owner_or_owner(fn):
    '''
    the authorised user is not an owner of the slackr, or an owner of this channel
    '''
    def wrapper(*args, **kwargs):
        channel_id = kwargs['channel_id']
        u_id = kwargs['u_id']

        # Get the corresponding channel with the id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Is user the owner of slakr?
        owner_of_slackr = (u_id == 0)

        # Is the user an owner of the channel?
        owner_of_channel = u_id in channel_with_id.get_owner_u_id_list()

        # If both these conditions are false, raise an error.
        if not (owner_of_slackr or owner_of_channel):
            raise error.AccessError('User is not an owner of the slackr, or an owner of this channel')

        # Else, return the function
        return fn(*args, **kwargs)

    return wrapper


def user_not_member_using_message_id(fn):
    '''
    The authorised user is not a member of the channel that the message is within.
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']
        message_id = kwargs['message_id']

        # Get user using token.
        user = data.get_data().get_user_with_token(token)

        # Get the user id using the User Class
        u_id = user.get_u_id()

        # Get the channel using message id.
        channel_with_id = data.get_data().get_channel_with_message_id(message_id)

        # Check if user is in the channel. If not, return error.
        if not u_id in channel_with_id.get_u_id_list():
            raise error.AccessError('The user is not a member of the channel that the message is within.')

        # If not, return the function
        return fn(*args, **kwargs)

    return wrapper

def edit_permissions(fn):
    '''
    AccessError when none of the following are true:

    1. Message with message_id was sent by the authorised user making this request

    2. The authorised user is an admin or owner of this channel or the slackr

    TODO: Figure out how to test for admin rights.
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']
        token = kwrags['token']

        # Get the user class using the token
        user = data.get_data().get_user_with_token(token)

        # Get the Message class using the message_id
        message = data.get_data().get_message_with_message_id(message_id)

        # Check if the message was sent by the user by comparing u_ids
        sent_by_user = user.get_u_id() == message.get_u_id()

        # Check if user is an admin or owner of slakr
        admin_or_owner = user.get_u_id() == 0 # TODO: Add check for admin.

        # Check if user is a owner of the channel. First get channel.
        channel = data.get_data().get_channel_with_message_id(message_id)
        
        # Check if his u_id is in the list of owners
        owner_of_channel = user.get_u_id() in channel.get_owner_u_id_list()

        # If none of these conditions are true. Raise access error
        if not (sent_by_user or admin_or_owner or owner_of_channel):
            raise error.AccessError('User does not have edit permissions')

        # Else, return function
        return fn(*args, **kwargs)

    return wrapper

def is_admin_or_owner(fn):
    '''
    The authorised user is not an admin or owner
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']
        u_id = kwargs['u_id']

        # Check if user is owner of slakr
        owner_of_slackr = u_id == 0

        # Check if user is an admin
        # TODO: Figure this out and change it.
        admin_of_slackr = False 

        if not (owner_of_slackr or admin_of_slackr):
            raise error.AccessError('The authorised user is not an admin or owner')

        return fn(*args, **kwargs)

    return wrapper

######################## Input Errors ########################



def valid_email(fn):
    '''
    Email entered is not a valid email.
    '''
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # Check the email form
        valid_email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(valid_email_regex, email):
            raise error.InputError('Email entered is not a valid email.')

        return fn(*args, **kwargs)

    return wrapper


def email_does_not_exist(fn):
    '''
    Email entered does not belong to a user
    '''
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # If it doesn't exist, raise an error
        if not data.get_data().get_user_with_email(email):
            raise error.InputError('Email entered does not belong to a user.')

        return fn(*args, **kwargs)
        
    return wrapper



def authenticate_password(fn):
    '''
    Password is not correct

    # TODO: Get Dan to figure this out. I have no clue about this salt
    '''
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
    '''
    Email address is already being used by another user.
    '''
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # If it email is already used, raise an error
        if data.get_data().get_user_with_email(email):
            raise error.InputError('Email address is already being used by another user.')

        return fn(*args, **kwargs)

    return wrapper

def check_password_length(fn):
    '''
    Password entered is less than 6 characters long.
    '''
    def wrapper(*args, **kwargs):

        # Get the password
        password = kwargs['password']

        if len(password) < 6:
            raise error.InputError('Password entered is less than 6 characters long.')

        return fn(*args, **kwargs)

    return wrapper

def check_name_length(fn):
    '''
    name_first is not between 1 and 50 characters inclusive in length

    name_last is not between 1 and 50 characters inclusive in length
    '''
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
    '''
    channel_id does not refer to a valid channel that the authorised user is part of.
    '''
    def wrapper(*args, **kwargs):
        
        # Get the channel id and user id in reference
        channel_id, u_id = kwargs['channel_id'], kwargs['u_id']

        # Find the channel respective to the u_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)
        
        # Now we either have a channel or not. If its empty, invalid. Else we need to check if user is in it
        if not channel_with_id:
            raise error.InputError('The channel does not exist.')

        # Now we are in a situation where we have an actual channel. Now to check if user is in it.
        if not u_id in channel_with_id.get_u_id_list():
             raise error.InputError('The user is not in this channel.')

        return fn(*args, **kwargs)
    
    return wrapper

def check_u_id_existance(fn):
    '''
    u_id does not refer to a valid user.

    User with u_id is not a valid user.
    '''
    def wrapper(*args, **kwargs):
        # Get user id
        u_id = kwargs['u_id']

        # Check if user_id exists
        if not data.get_data().get_user_with_u_id(u_id):
            raise error.InputError(f'u_id: {u_id} does not refer to a valid user.')

        return fn(*args, **kwargs)

    return wrapper

def valid_channel_id(fn):
    '''
    Channel ID is not a valid channel
    '''
    def wrapper(*args, **kwargs):

        # Get channel id
        channel_id = kwargs['channel_id']

        # Check if channel_id exists
        if not data.get_data().get_channel_with_ch_id(channel_id):
            raise error.InputError(f'Channel ID: {channel_id} is not a valid channel.')

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

        # Get the channel with the id in question.
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Now we either have a channel or not. If its empty, invalid. Else we need to check if user is in it
        if not channel_with_id:
            raise error.InputError('The channel does not exist.')
        
        # Now inital condition.
        if start >= len(channel_with_id.get_msg_id_list()):
            raise error.InputError('Start is greater than or equal to the total number of messages in the channel.')

        return fn(*args, **kwargs)
    
    return wrapper


def already_owner(fn):
    '''
    When user with user id u_id is already an owner of the channel.
    '''

    def wrapper(*args, **kwargs):

        # Get user and channel id
        u_id, channel_id = kwargs['u_id'], kwargs['channel_id']

        # Get channel with channel_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Get a list of the owners
        owner_ids = channel_with_id.get_owner_u_id_list()

        # Check if the user is an owner
        if u_id in owner_ids:
            raise error.InputError(f'The user with user id {u_id} is already an owner of the channel')

        return fn(*args, **kwargs)

    return wrapper

def not_owner(fn):
    '''
    When user with user id u_id is not an owner of the channel
    '''

    def wrapper(*args, **kwargs):
        # Get user and channel id
        u_id, channel_id = kwargs['u_id'], kwargs['channel_id']

        # Get channel with channel_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Get a list of the owners
        owner_ids = channel_with_id.get_owner_u_id_list()

        # Check if the user is an owner
        if not u_id in owner_ids:
            raise error.InputError(f'The user with user id {u_id} is not an owner of the channel')

        return fn(*args, **kwargs)

    return wrapper

def user_not_admin(fn):
    '''
    The authorised user is not an admin

    TODO: How to check if user is an admin?
    TODO: Check on piazza. This seems more like an access error than input error.
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']

        # TODO Do check if user is an admin.
        is_admin = False

        # If not admin, raise input error? TODO: check that. should be access
        if not is_admin:
            raise error.InputError('The authorised user is not an admin')

        return fn(*args, **kwargs):

    return wrapper

def channel_name_length(fn):
    '''
    Name is more than 20 characters long.
    '''
    def wrapper(*args, **kwargs):

        # Get channel name
        channel_name = kwargs['name']

        if len(channel_name) > 20:
            raise error.InputError('Name is more than 20 characters long.')

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
        time_sent = kwargs['time_sent']

        if time_sent < time.time():
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
        token = kwargs['token']

        # Get the channel corresponding to the message id
        channel_with_id = data.get_data().get_channel_with_message_id(message_id)

        # Get user from token
        user = data.get_data().get_user_with_token(token)
        
        # Check if the user is in the channel. If not, raise an error
        if not user.get_u_id() in channel_with_id.get_u_id_list():
            raise error.InputError(f'{message_id} is not a valid message within a channel that the authorised user has joined.')

        # If he is in the channel. Proceed.
        return fn(*args, **kwargs)

    return wrapper

def is_valid_react_id(fn):
    '''
    react_id is not a valid React ID. The only valid react ID the frontend has is 1
    '''
    def wrapper(*args, **kwargs):

        react_id = kwargs['react_id']

        if react_id != 1:
            raise error.InputError(f'{react_id} is not a valid React ID. The only valid react ID is 1')

        return fn(*args, **kwargs)

    return wrapper

def already_contains_react(fn):
    '''
    Message with ID message_id already contains an active React with ID react_id
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']
        react_id = kwargs['react_id']

        # Get message with message_id
        message_with_id = data.get_data().get_message_with_message_id(message_id)

        # If the react is in the list. Raise an error.
        if react_id in message_with_id.get_react_list():
            raise error.InputError(f'Message with ID {message_id} already contains an active React with ID {react_id}')

        # Else, return the function
        return fn(*args, **kwargs)

    return wrapper

def does_not_contain_react(fn):
    '''
    Message with ID message_id does not contain an active React with ID react_id
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']
        react_id = kwargs['react_id']

        # Get message with message_id
        message_with_id = data.get_data().get_message_with_message_id(message_id)

        # If the react is not in the list. Raise an error
        if not react_id in message_with_id.get_react_list():
            raise error.InputError(f'Message with ID {message_id} does not contain an active React with ID {react_id}')
        
        # Else, return the function
        return fn(*args, **kwargs)

    return wrapper

def message_id_valid(fn):
    '''
    message_id is not a valid message.

    Message (based on ID) no longer exists.
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']

        # Get message with the message id
        message_with_id = data.get_data().get_message_with_message_id(message_id)

        # Check if the message id exists.
        if not message_with_id:
            raise error.InputError(f'{message_id} is not a valid message or does not exist anymore.')

        # Else, return the function
        return fn(*args, **kwargs)

    return wrapper

def message_already_pinned(fn):
    '''
    Message with ID message_id is already pinned
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']

        # Get message with the message id.
        message_with_id = data.get_data().get_message_with_message_id(message_id)

        # If message is already pinned. Raise an error.
        if message_with_id.get_is_pinned():
            raise error.InputError(f'Message with ID {message_id} is already pinned')

        # Else return the function.
        return fn(*args, **kwargs)

    return wrapper

def message_already_unpinned(fn):
    '''
    Message with ID message_id is already unpinned
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']

        # Get message with the message id.
        message_with_id = data.get_data().get_message_with_message_id(message_id)

        # If message is not pinned. Raise an error.
        if not message_with_id.get_is_pinned():
            raise error.InputError(f'Message with ID {message_id} is already unpinned')
        
        # Else return the function.
        return fn(*args, **kwargs)

    return wrapper


def handle_length(fn):
    '''
    handle_str must be between 2 and 20 characters inclusive.
    '''
    def wrapper(*args, **kwargs):
        handle_str = kwargs['handle_str']

        if not (2 <= len(handle_str) <= 20):
            raise error.InputError('handle_str must be between 2 and 20 characters inclusive.')

        return fn(*args, **kwargs)

    return wrapper

def handle_already_used(fn):
    '''
    handle is already used by another user.
    '''
    def wrapper(*args, **kwargs):
        handle_str = kwargs['handle_str']

        # Try to get a user with the handle_str.
        user_with_handle = data.get_data().get_user_with_handle_str(handle_str)

        # If we get a user. Raise an error.
        if user_with_handle:
            raise error.InputError('Handle is already used by another user.')

        # Else, return the function.
        return fn(*args, **kwargs)

    return wrapper

def already_active_standup(fn):
    # TODO get help. 
    '''
    An active standup is currently running in this channel
    '''
    pass

def no_active_standup(fn):
    # TODO get help.
    '''
    An active standup is not currently running in this channel
    '''
    pass

def permission_id(fn):
    # TODO get help.
    '''
    permission_id does not refer to a value permission
    '''
    pass




#### Authenticator function ####

def authenticator(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco