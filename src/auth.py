"""
Authentication module that handles the login, logout and register of users.
"""
import authenticate as au
import auth_helper
import data


@au.valid_email
@au.email_does_not_exist
@au.authenticate_password
def auth_login(*, email, password):
    """
    Logs the user in with email and password.
    Returns the user's u_id and token.
    """
    # Get the u_id from the email
    u_id = data.get_data().get_user_with_email(email).get_u_id()

    # Generate a new token for the new login sessino
    token = auth_helper.generate_token()

    # Create the login object
    new_login = data.Login(u_id, token)

    # Add the login object to data
    data.get_data().add_login(new_login)

    # Return user id and valid token
    return data.get_data().get_login_with_token(token).get_login_dict()


@au.is_token_valid
def auth_logout(*, token):
    """
    Logs the user out with just the token.
    The token becomes invalidated.
    """
    # Successful logout is false
    is_success = False

    # Get the login object associated with the given token
    login_remove = data.get_data().get_login_with_token(token)

    # Remove the login object from the list of logins
    data.get_data().remove_login(login_remove)

    # Generate list of valid tokens
    valid_tokens = map(lambda login: login.get_token(),
                       data.get_data().get_login_list())

    # Successful logout is true
    if not token in valid_tokens:
        is_success = True

    return {'is_success': is_success}


@au.valid_email
@au.email_already_used
@au.check_name_length
def auth_register(*, email, password, name_first, name_last):
    """
    Registers the user. Several processes occur in this function: the user id,
    salt, hash, handle is created. A password, user object is created
    and stored in data. Returns the call to auth_login.
    """
    # Get the user id
    u_id = data.get_data().global_u_id()

    # Generate the hashed password for the new user
    salt, hash_ = auth_helper.generate_hash(password)

    # Instantiate Password (object)
    hashed_password = data.Password(u_id, salt, hash_)

    # Store Password object in data
    data.get_data().add_password(hashed_password)

    # Generate the handle string
    handle_str = auth_helper.generate_handle(u_id, name_first, name_last)

    # Instantiate User (object)
    new_user = data.User(u_id, email, name_first, name_last, handle_str)

    # Add this new user to the list of users
    data.get_data().add_user(new_user)

    # Log the user in after registration
    return auth_login(email=email, password=password)
