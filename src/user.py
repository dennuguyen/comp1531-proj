'''
user.py has four main functions.

user_profile(.) - returns a user dictionary given a u_id

user_profile_setname(.) - allows updating of first and last names

user_profile_setemail(.) - allows updating of email.

user_profile_sethandle(.) - allows updating of handles.
'''

import data
import authenticate as au

@au.authenticator(au.is_token_valid, au.check_u_id_existence)
def user_profile(*, token, u_id):
    '''
    For a valid user, returns information about their user id, email,
    first name, last name, and handle.
    '''
    # Get the User dataclass with u_id.
    user = data.get_data().get_user_with_u_id(u_id)
    return {'user' : user.get_user_dict()}

@au.authenticator(au.is_token_valid, au.check_name_length)
def user_profile_setname(*, token, name_first, name_last):
    '''
    Update the authorised user's first and last name.
    '''
    # Get user class with token
    user = data.get_data().get_user_with_token(token)

    # Update the corresponding name
    user.set_name_first(name_first)
    user.set_name_last(name_last)

    return {}

@au.authenticator(au.is_token_valid, au.valid_email, au.email_already_used)
def user_profile_setemail(*, token, email):
    '''
    Update the authorised user's email address.
    '''
    # Get user class with token
    user = data.get_data().get_user_with_token(token)

    # Update the corresponding email
    user.set_email(email)

    return {}

@au.authenticator(au.is_token_valid, au.handle_length, au.handle_already_used)
def user_profile_sethandle(*, token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name).
    '''
    # Get user class with token
    user = data.get_data().get_user_with_token(token)

    # Update the corresponding handle_str
    user.set_handle_str(handle_str)

    return {}
