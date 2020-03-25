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


# Case where the user is not a member of the channel thus raising an AccessError
# This case is observed in the following functions:
#   channel_invite
#   channel_details
#   channel_messages
#   channel_leave
#   message_send
#   message_sendlater
#   message_pin
#   message_unpin
#   message_remove
#   standup_send
# Token and channel id are obtained from these functions


#### ACCESS ERRORS ####

def is_not_member(fn):
    '''
    Authorised user is not a member of channel with channel_id.
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']
        channel_id = kwargs['channel_id']

        

def is_member(fn):
    '''

    '''
    def wrapper(*args, **kwargs):

        # Get the token
        token = kwargs['token']
        ch_id = kwargs['ch_id']

        # Check if token exists #TODO since this is every access erorr. We should decorate
        is_token_valid(token)

        # Check if user is member of channel
        for member in data.getData().):            ######## TO DO: get this from data.py
            if token == member['token']
                return fn(*args, **kwargs)

        # If cannot find a token, then raise AccessError
        raise error.AccessError

    return wrapper

# Decorator function where a user with a valid u_id cannot join a private channel
# Channel id is obtained from channel_join()
def is_private(fn):
    def wrapper(*args, **kwargs):

        # Get the token
        token = kwargs['token']
        ch_id = kwargs['ch_id']

        # Check if token exists
        is_token_valid(token)

        # Check if channel is private
        # If cannot find a token, then raise AccessError
        if not data.Channels.is_private(ch_id):                 ######## TO DO: get this from data.py
            raise error.AccessError

        return fn(*args, **kwargs)

    return wrapper

# Case where a user is not an owner. This case is observed in the folllowing
# functions:
#   channel_addowner()
#   channel_removeowner()
#   admin_userpermission_change (this is a route)
# Token and channel id is obtained from these functions
def is_owner(fn):
    def wrapper(*args, **kwargs):

        # Get the token
        token = kwargs['token']
        ch_id = kwargs['ch_id']

        # Check if token exists
        is_token_valid(token)

        # Check if user is an owner
        for member in data.Channels.get_owners(ch_id):          ######## TO DO: get this from data.py
            if token == member['token']
                return fn(*args, **kwargs)

        # If cannot find a token, then raise AccessError
        raise error.AccessError

    return wrapper


# Case where user is not an owner or user who sent the message to have
# permissions to edit or remove the message:
#   message remove()
#   message edit()
# Token and message id is obtained from these functions
def is_message_permission(fn):
    def wrapper(*args, **kwargs):

        # Get the token
        token = kwargs['token']
        msg_id = kwargs['msg_id']

        # Check if token exists
        is_token_valid(token)

        # Search channels which have msg_id to edit/remove
        for channel in data.channels:
            if msg_id == channel.get_msg(msg_id):
                # Get the channel id to search for channel owners
                ch_id = channel['ch_id']
                for member in data.Channels.get_owners(ch_id):     ######## TO DO: get this from data.py
                    if token == member['token']
                        return fn(*args, **kwargs)
                
                break

        # Check if user sent the message to edit/remove
        for channel in data.channels.get_channel(ch_id):        ######## TO DO: get this from data.py
            if token == channel.get_msg(msg_id)['token']        ######## TO DO: get this from data.py
                return fn(*args, **kwargs)

        # If user removing message did not create the message then
        raise error.AccessError

    return wrapper


# Case where token is not owner of slackr raises access error
def is_owner_of_slackr(fn):
    # TODO check u_id allocations that slackr owner is u_id 0
    '''
    The authorised user is not an owner of slackr raise access error
    '''
        def wrapper(*args, **kwargs):

        # Get the token
        token = kwargs['token']

        # Check if token exists
        is_token_valid(token)

        # Check if user is an owner
        u_id = data.Login.get_u_id_with_token(token):          ######## TO DO: get this from data.py
        if  u_id == 0
            return fn(*args, **kwargs)

        # If cannot find a token, then raise AccessError
        raise error.AccessError

    return wrapper

    pass


def is_sender(fn):
    # TODO check unauthorised user
    '''
    Message operation was not by authorised user, raise access error
    '''
        def wrapper(*args, **kwargs):

        # Get the token
        token = kwargs['token']
        message_id = kwargs['message_id']
        u_id = kwargs['u_id']

        # Check if token exists
        is_token_valid(token)

        # Check if user is an owner
        for message in data.message_list:          ######## TO DO: get this from data.py
            if message.get_message_dict(message_id)['message_id'] == message_id:
                if message.get_message_dict(message_id)['u_id'] == u_id
                    return fn(*args, **kwargs)

        # If cannot find a token, then raise AccessError
        raise error.AccessError

    return wrapper
    pass

######################## Input Errors #######################3



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
    name_first not is between 1 and 50 characters inclusive in length

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
    # TODO Get help for this one

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