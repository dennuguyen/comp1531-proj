'''
This file is composed of many decorator functions aimed to check specific
"Input Error" cases and "Access Error" cases.

If the function you are writing for has an Input or Access error condition.
For example "Email entered does not belong to a user".
Control + F to search for the function required to test for it then follow the example below.



EXAMPLES ON USE:

The use of this ultimate decorator is quite simple.
I will show an example on how to check for all input errors in the first function: "auth/login"

import authenticate as au

@au.authenticator(au.token, au.valid_email, au.email_does_not_exist, au.authenticate_password)
def login():
    pass
'''

# Standard imports
import re
import time

# File imports
import error
import data
import auth_helper

################################################################################
#                                                                              #
#                                Access ERRORS                                 #
#                                                                              #
################################################################################


def is_token_valid(func):
    '''
    token passed in is not a valid token
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']

        # Get a list of all those who are logged in
        logged_in_list = data.get_data().get_login_list()

        # Get a map variable of all valid tokens.
        valid_tokens = map(lambda logged_in_user: logged_in_user.get_token(),
                           logged_in_list)

        #print(token)
        #print(list(valid_tokens)) # The result is []
        # If the token is not in the list (technically mapping) of valid tokens. Raise Error.
        if not token in list(valid_tokens):
            raise error.AccessError('token passed in is not a valid token')

        # Else, return the function.
        return func(*args, **kwargs)

    return wrapper


def is_not_member(func):
    '''
    Authorised user is not a member of channel with channel_id.

    the authorised user has not joined the channel they are trying to post to.

    the authorised user is not already a member of the channel
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']
        channel_id = kwargs['channel_id']

        # Get the corresponding user with the token.
        user = data.get_data().get_user_with_token(token)
        
        # Get corresponding channel with the channel_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)
        # Check if user is in the channel. If not, raise an error.
        if not user.get_u_id() in channel_with_id.get_u_id_list():
            raise error.AccessError(
                f"Error: User {user.get_u_id()} is not a member of channel with {channel_id}")

        # Else, return the function
        return func(*args, **kwargs)

    return wrapper


def is_private_not_admin(func):
    '''
    channel_id refers to a channel that is private (when the authorised user is not an admin)

    TODO: Unable to complete since I don't know the definition of admin.
    '''
    def wrapper(*args, **kwargs):
        channel_id = kwargs['channel_id']
        token = kwargs['token']

        # Get User class with token
        user_with_token = data.get_data().get_user_with_token(token)

        # Get Channel class with channel_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Check if user is admin TODO: Complete this
        is_admin = False  # False by default.

        # If the user is not an admin. We check if the channel is private.
        # If private, raise an error
        if not is_admin:
            if not channel_with_id.get_is_public():
                error_message = '''
                channel_id refers to a channel that is private (when the authorised user is not an admin)
                '''
                raise error.AccessError(error_message)

        return func(*args, **kwargs)

    return wrapper


def is_owner_or_slackr_owner(func):
    '''
    the authorised user is not an owner of the slackr, or an owner of this channel
    '''
    def wrapper(*args, **kwargs):
        channel_id = kwargs['channel_id']
        token = kwargs['token']

        # Get user_id from token
        user = data.get_data().get_user_with_token(token)
        u_id = user.get_u_id()

        # Get the corresponding channel with the id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Is user the owner of slakr?
        owner_of_slackr = (u_id == 0)

        # Is the user an owner of the channel?
        owner_of_channel = u_id in channel_with_id.get_owner_u_id_list()

        # If both these conditions are false, raise an error.
        if not (owner_of_slackr or owner_of_channel):
            error_message = 'User is not an owner of the slackr, or an owner of this channel'
            raise error.AccessError(error_message)

        # Else, return the function
        return func(*args, **kwargs)

    return wrapper

def is_owner_or_slackr_owner_1(func):
    '''
    the authorised user is not an owner of the slackr, or an owner of this channel
    '''
    def wrapper(*args, **kwargs):

        msg_id = kwargs['message_id']
        token = kwargs['token']

        # Get user_id from token
        user = data.get_data().get_user_with_token(token)
        u_id = user.get_u_id()

        # Check if the message and the user are in the same channel while the user is an owner
        flag = False
        for channel in data.get_data().get_channel_list():
            if u_id in channel.get_owner_u_id_list() and msg_id in channel.get_msg_id_list():
                flag = True
        if not flag:
            error_message = 'User is not an owner of the slackr, or an owner of this channel'
            raise error.AccessError(error_message)
        
        # Else, return the function
        return func(*args, **kwargs)

    return wrapper


def user_not_member_using_message_id(func):
    '''
    The authorised user is not a member of the channel that the message is within.
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']
        message_id = kwargs['message_id']

        # Get user using token.
        user_with_token = data.get_data().get_user_with_token(token)

        # Get the user id using the User Class
        u_id = user_with_token.get_u_id()

        # Get the channel using message id.
        channel_with_id = data.get_data().get_channel_with_message_id(
            message_id)

        # Check if user is in the channel. If not, return error.
        if not u_id in channel_with_id.get_u_id_list():
            error_message = '''
            The user is not a member of the channel that the message is within.
            '''
            raise error.AccessError(error_message)

        # If not, return the function
        return func(*args, **kwargs)

    return wrapper


def edit_permissions(func):
    '''
    AccessError when none of the following are true:

    1. Message with message_id was sent by the authorised user making this request

    2. The authorised user is an admin or owner of this channel or the slackr

    TODO: Figure out how to test for admin rights.
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']
        token = kwargs['token']
        print(message_id)
        # Get the user class using the token
        token_uid = data.get_data().get_user_with_token(token).get_u_id()

        # Get the Message class using the message_id
        message_uid = data.get_data().get_message_with_message_id(message_id).get_u_id()

        # Check if the message was sent by the user by comparing u_ids
        sent_by_user = token_uid == message_uid

        # Check if user is an admin or owner of slakr
        admin_or_owner = token_uid == 0  # TODO: Add check for admin.

        # Check if user is a owner of the channel. First get channel.
        channel = data.get_data().get_channel_with_message_id(message_id)

        # Check if his u_id is in the list of owners
        owner_of_channel = token_uid in channel.get_owner_u_id_list()

        # If none of these conditions are true. Raise access error
        if not (sent_by_user or admin_or_owner or owner_of_channel):
            raise error.AccessError('User does not have edit permissions')

        # Else, return function
        return func(*args, **kwargs)

    return wrapper


def is_admin_or_owner(func):
    '''
    The authorised user is not an admin or owner
    '''
    def wrapper(*args, **kwargs):
        u_id = kwargs['u_id']

        # Check if user is owner of slakr
        owner_of_slackr = u_id == 0

        # Check if user is an admin
        # TODO: Figure this out and change it.
        admin_of_slackr = False

        if not (owner_of_slackr or admin_of_slackr):
            raise error.AccessError(
                'The authorised user is not an admin or owner')

        return func(*args, **kwargs)

    return wrapper


################################################################################
#                                                                              #
#                               INPUT ERRORS                                   #
#                                                                              #
################################################################################


def valid_email(func):
    '''
    Email entered is not a valid email.
    '''
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # Check the email form
        valid_email_regex = r'[\w+g]{1,64}[@][\w+g+\.]{1,255}$'

        if not re.match(valid_email_regex, email):
            raise error.InputError('Error: invalid email.')

        return func(*args, **kwargs)

    return wrapper


def email_does_not_exist(func):
    '''
    Email entered does not belong to a user
    '''
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # If it doesn't exist, raise an error
        if not data.get_data().get_user_with_email(email):
            raise error.InputError('Error: email does not exist.')

        return func(*args, **kwargs)

    return wrapper


def email_already_used(func):
    '''
    Email address is already being used by another user.
    '''
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email']

        # If it email is already used, raise an error
        if data.get_data().get_user_with_email(email):
            raise error.InputError(
                'Email address is already being used by another user.')

        return func(*args, **kwargs)

    return wrapper


def authenticate_password(func):
    """
    Password is authenticated by retrieving the salt for the user, hashing the
    password with the salt, then comparing the hashed password with existing
    hashed passwords stored in the password database.

            email
              |
              V
            u_id        try_password
              |             |
              V             V
            salt  --> hash_it(salt, try_password)
                            |
                            V
                        try_hash
                            |
                            V
            try_hash == get_password_with_hash(try_hash).get_hash()
    """

    # TODO for iteration 3, separate the salt + u_id data from password data
    def wrapper(*args, **kwargs):

        # Get the email and password
        email = kwargs['email']
        try_password = kwargs['password']

        # Get the user id from getting the user object with email
        u_id = data.get_data().get_user_with_email(email).get_u_id()

        # Get the salt from getting the password object with user id
        salt = data.get_data().get_password_with_u_id(u_id).get_salt()

        # Hash the given password with the stored salt
        try_hash = auth_helper.hash_it(salt, try_password)

        # Try hash comparison with the stored hash
        try:
            strd_hash = data.get_data().get_password_with_hash(
                try_hash).get_hash()

            if try_hash != strd_hash:
                raise error.InputError("Incorrect password")
        except Exception:
            raise error.InputError("Incorrect password")

        return func(*args, **kwargs)

    return wrapper


def check_password_length(func):
    '''
    Password entered is less than 6 characters long.
    '''
    def wrapper(*args, **kwargs):

        # Get the password
        password = kwargs['password']

        if len(password) < 6:
            raise error.InputError(
                'Password entered is less than 6 characters long.')

        return func(*args, **kwargs)

    return wrapper


def check_name_length(func):
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
            error_message = '''
            First and last name must be between 1 and 50 characters inclusive.
            '''
            raise error.InputError(error_message)

        return func(*args, **kwargs)

    return wrapper


def is_user_in_channel(func):
    '''
    channel_id does not refer to a valid channel that the authorised user is part of.
    '''
    def wrapper(*args, **kwargs):

        # Get the channel id and user id in reference
        channel_id, u_id = kwargs['channel_id'], kwargs['u_id']

        # Find the channel respective to the u_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Now we either have a channel or not.
        # If its empty, invalid. Else we need to check if user is in it
        if not channel_with_id:
            raise error.InputError('The channel does not exist.')

        # Now we are in a situation where we have an actual channel. Now to check if user is in it.
        if u_id not in channel_with_id.get_u_id_list():
            raise error.InputError('The user is not in this channel.')

        return func(*args, **kwargs)

    return wrapper

def is_token_in_channel(func):
    '''
    channel_id does not refer to a valid channel that the authorised user is part of.
    '''
    def wrapper(*args, **kwargs):

        # Get the channel id and user id in reference
        channel_id, token = kwargs['channel_id'], kwargs['token']

        u_id = data.get_data().get_user_with_token(token).get_u_id()

        # Find the channel respective to the u_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Now we either have a channel or not.
        # If its empty, invalid. Else we need to check if user is in it
        if not channel_with_id:
            raise error.InputError('The channel does not exist.')

        # Now we are in a situation where we have an actual channel. Now to check if user is in it.
        if u_id not in channel_with_id.get_u_id_list():
            raise error.AccessError('The user is not in this channel.')

        return func(*args, **kwargs)

    return wrapper

def is_token_not_in_channel(func):
    '''
    channel_id does not refer to a valid channel that the authorised user is part of.
    '''
    def wrapper(*args, **kwargs):

        # Get the channel id and user id in reference
        channel_id, token = kwargs['channel_id'], kwargs['token']

        u_id = data.get_data().get_user_with_token(token).get_u_id()

        # Find the channel respective to the u_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Now we either have a channel or not.
        # If its empty, invalid. Else we need to check if user is in it
        if not channel_with_id:
            raise error.InputError('The channel does not exist.')

        # Now we are in a situation where we have an actual channel. Now to check if user is in it.
        if u_id in channel_with_id.get_u_id_list():
            raise error.InputError('The user is in this channel.')

        return func(*args, **kwargs)

    return wrapper

def is_user_not_in_channel(func):
    '''
    channel_id refer to a valid channel that the authorised user is part of.
    '''
    def wrapper(*args, **kwargs):

        # Get the channel id and user id in reference
        channel_id, u_id = kwargs['channel_id'], kwargs['u_id']

        # Find the channel respective to the u_id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Now we either have a channel or not.
        # If its empty, invalid. Else we need to check if user is in it
        if not channel_with_id:
            raise error.InputError('The channel does not exist.')

        # Now we are in a situation where we have an actual channel. Now to check if user is in it.
        if u_id in channel_with_id.get_u_id_list():
            raise error.InputError('The user is in this channel.')

        return func(*args, **kwargs)

    return wrapper

def is_not_slackr_owner(func):
    '''
    the authorised user is an owner of the slackr
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']

        # Get user_id from token
        user = data.get_data().get_user_with_token(token)


        # If user the owner of slakr, raise an error.
        if user.get_u_id() == 0:
            error_message = 'User is an owner of the slackr'
            raise error.InputError(error_message)

        # Else, return the function
        return func(*args, **kwargs)

    return wrapper

def check_u_id_existence(func):
    '''
    u_id does not refer to a valid user.

    User with u_id is not a valid user.
    '''
    def wrapper(*args, **kwargs):
        # Get user id
        u_id = kwargs['u_id']

        # Check if user_id exists
        if not data.get_data().get_user_with_u_id(u_id):
            raise error.InputError(
                f'u_id: {u_id} does not refer to a valid user.')

        return func(*args, **kwargs)

    return wrapper


def valid_channel_id(func):
    '''
    Channel ID is not a valid channel
    '''
    def wrapper(*args, **kwargs):

        # Get channel id
        channel_id = kwargs['channel_id']

        # Check if channel_id exists
        if not data.get_data().get_channel_with_ch_id(channel_id):
            raise error.InputError(
                f'Channel ID: {channel_id} is not a valid channel.')

        return func(*args, **kwargs)

    return wrapper


def start_has_more_messages(func):
    '''
    start is greater than or equal to the total number of messages in the channel
    '''
    def wrapper(*args, **kwargs):

        # Get start number
        start = kwargs['start']
        channel_id = kwargs['channel_id']

        # Get the channel with the id in question.
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Now we either have a channel or not.
        # If its empty, invalid. Else we need to check if user is in it
        if not channel_with_id:
            raise error.InputError('The channel does not exist.')

        # Now inital condition.
        if start > len(channel_with_id.get_msg_id_list()):
            error_message = '''
            Start is greater than or equal to the total number of messages in the channel.
            '''
            raise error.InputError(error_message)

        return func(*args, **kwargs)

    return wrapper


def already_owner(func):
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
            error_message = f'''
            The user with user id {u_id} is already an owner of the channel
            '''
            raise error.InputError(error_message)

        return func(*args, **kwargs)

    return wrapper


def not_owner(func):
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
            raise error.InputError(
                f'The user with user id {u_id} is not an owner of the channel')

        return func(*args, **kwargs)

    return wrapper


def user_not_admin(func):
    '''
    The authorised user is not an admin

    TODO: How to check if user is an admin?
    TODO: Check on piazza. This seems more like an access error than input error.
    '''
    def wrapper(*args, **kwargs):

        # TODO Do check if user is an admin.
        is_admin = False

        # If not admin, raise input error? TODO: check that. should be access
        if not is_admin:
            raise error.InputError('The authorised user is not an admin')

        return func(*args, **kwargs)

    return wrapper


def channel_name_length(func):
    '''
    Name is more than 20 characters long or empty string.
    '''
    def wrapper(*args, **kwargs):

        # Get channel name
        channel_name = kwargs['name']


        flag = channel_name.isspace()

        if len(channel_name) > 20 or channel_name == '' or flag is True:
            raise error.InputError('Name is not valid: Must be less 20 characters and not empty or made up of spaces.')



        return func(*args, **kwargs)

    return wrapper


def message_length(func):
    '''
    Message is more than 1000 characters
    '''
    def wrapper(*args, **kwargs):

        # Get message
        message = kwargs['message']

        if len(message) > 1000:
            raise error.InputError('Message is more than 1000 characters.')

        return func(*args, **kwargs)

    return wrapper


def send_message_in_future(func):
    '''
    Time sent is a time in the past
    '''
    def wrapper(*args, **kwargs):
        time_sent = kwargs['time_sent']

        if time_sent < time.time():
            raise error.InputError('Time sent is a time in the past')

        return func(*args, **kwargs)

    return wrapper


def is_message_id_in_channel(func):
    '''
    message_id is not a valid message within a channel that the authorised user has joined
    '''
    def wrapper(*args, **kwargs):

        # Get message id and channel_id
        message_id = kwargs['message_id']
        token = kwargs['token']

        # Get the channel corresponding to the message id
        channel_with_id = data.get_data().get_channel_with_message_id(
            message_id)

        # Get user from token
        user_with_token = data.get_data().get_user_with_token(token)

        # Check if the user is in the channel. If not, raise an error
        if not channel_with_id or not user_with_token.get_u_id() in channel_with_id.get_u_id_list():
            error_message = f'''
            {message_id} is not a valid message within a channel that the authorised user has joined.
            '''
            raise error.InputError(error_message)

        # If he is in the channel. Proceed.
        return func(*args, **kwargs)

    return wrapper


def is_valid_react_id(func):
    '''
    react_id is not a valid React ID. The only valid react ID the frontend has is 1
    '''
    def wrapper(*args, **kwargs):

        react_id = kwargs['react_id']

        if react_id != 1:
            error_message = f'''
            {react_id} is not a valid React ID. The only valid react ID is 1.
            '''
            raise error.InputError(error_message)

        return func(*args, **kwargs)

    return wrapper


def already_contains_react(func):
    '''
    Message with ID message_id already contains an active React with ID react_id
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']
        react_id = kwargs['react_id']

        # Get message with message_id
        message = data.get_data().get_message_with_message_id(
            message_id)

        # If the react is already active
        if message.get_react_with_react_id(react_id).get_is_this_user_reacted():
            error_message = f'''
            Message with ID {message_id} already contains an active React with ID {react_id}
            '''
            raise error.InputError(error_message)

        # Else, return the function
        return func(*args, **kwargs)

    return wrapper


def does_not_contain_react(func):
    '''
    Message with ID message_id does not contain an active React with ID react_id
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']
        react_id = kwargs['react_id']

        # Get message with message_id
        message = data.get_data().get_message_with_message_id(
            message_id)

         # If the react is not active
        if not message.get_react_with_react_id(react_id).get_is_this_user_reacted():
            error_message = f'''
            Message with ID {message_id} does not contain an active React with ID {react_id}
            '''
            raise error.InputError(error_message)

        # Else, return the function
        return func(*args, **kwargs)

    return wrapper


def message_id_valid(func):
    '''
    message_id is not a valid message.

    Message (based on ID) no longer exists.
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']

        # Get message with the message id
        message_with_id = data.get_data().get_message_with_message_id(
            message_id)

        # Check if the message id exists.
        if not message_with_id:
            error_message = f'''
            {message_id} is not a valid message or does not exist anymore.
            '''
            raise error.InputError(error_message)

        # Else, return the function
        return func(*args, **kwargs)

    return wrapper


def message_already_pinned(func):
    '''
    Message with ID message_id is already pinned
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']

        # Get message with the message id.
        message_with_id = data.get_data().get_message_with_message_id(
            message_id)

        # If message is already pinned. Raise an error.
        if message_with_id.get_is_pinned():
            raise error.InputError(
                f'Message with ID {message_id} is already pinned')

        # Else return the function.
        return func(*args, **kwargs)

    return wrapper


def message_already_unpinned(func):
    '''
    Message with ID message_id is already unpinned
    '''
    def wrapper(*args, **kwargs):
        message_id = kwargs['message_id']

        # Get message with the message id.
        message_with_id = data.get_data().get_message_with_message_id(
            message_id)

        # If message is not pinned. Raise an error.
        if not message_with_id.get_is_pinned():
            raise error.InputError(
                f'Message with ID {message_id} is already unpinned')

        # Else return the function.
        return func(*args, **kwargs)

    return wrapper


def handle_length(func):
    '''
    handle_str must be between 2 and 20 characters inclusive.
    '''
    def wrapper(*args, **kwargs):
        handle_str = kwargs['handle_str']

        if not 2 <= len(handle_str) <= 20:
            raise error.InputError(
                'handle_str must be between 2 and 20 characters inclusive.')

        return func(*args, **kwargs)

    return wrapper


def handle_already_used(func):
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
        return func(*args, **kwargs)

    return wrapper


def already_active_standup(func):
    '''
    An active standup is currently running in this channel
    '''
    def wrapper(*args, **kwargs):
        channel_id = kwargs['channel_id']

        # Get the corresponding channel with the id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Check if there is an active standup in this channel
        if channel_with_id.get_is_active_standup():
            raise error.AccessError(
                'An active standup is currently running in this channel')

        return func(*args, **kwargs)

    return wrapper


def no_active_standup(func):
    '''
    An active standup is not currently running in this channel
    '''
    def wrapper(*args, **kwargs):
        channel_id = kwargs['channel_id']

        # Get the corresponding channel with the id
        channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

        # Check if there is not an active standup in this channel
        if not channel_with_id.get_is_active_standup():
            raise error.AccessError(
                'An active standup is currently running in this channel')

        return func(*args, **kwargs)

    return wrapper


def permission_id(func):
    # TODO get help.
    '''
    permission_id does not refer to a value permission
    '''
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


#### Extra Error checkers ####
def is_not_owner_of_slackr(func):
    '''
    Raise input error if uid is owner of slackr.
    '''
    def wrapper(*args, **kwargs):
        u_id = kwargs['u_id']

        # If the u_id is 0, this user is the owner of slackr. Raise error.
        if u_id == 0:
            raise error.InputError(
                'Raise input error if uid is owner of slackr.')

        return func(*args, **kwargs)

    return wrapper

def is_not_self(func):
    '''
    Raise input error if uid is owner of slackr.
    '''
    def wrapper(*args, **kwargs):
        token = kwargs['token']
        u_id = kwargs['u_id']
        token_uid = data.get_data().get_user_with_token(token).get_u_id()

        # If the u_id is 0, this user is the owner of slackr. Raise error.
        if u_id == token_uid:
            raise error.InputError(
                'Raise input error if token is self')

        return func(*args, **kwargs)

    return wrapper

#### Authenticator function ####


def authenticator(*decs):
    '''
    This function just combines multiple decorators into one.

    For example

    @dec1
    @dec2
    @dec3
    def func():
        pass

    is equivalent to

    @authenticator(dec1, dec2, dec3)
    def func():
        pass
    '''
    def deco(funcs):
        for dec in reversed(decs):
            funcs = dec(funcs)
        return funcs

    return deco
