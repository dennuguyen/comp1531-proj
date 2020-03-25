"""
Contains the helper functions for auth.py i.e. to generate a token, handle, and
hash.
"""
import hashlib
import string
import secrets
import data


def generate_token():
    """
    The token is generated using token_hex() from Python's secrets module.
    """
    return secrets.token_hex()


def generate_handle(u_id, name_first, name_last):
    """
    The handle is the concatentation of the lower case of the first name and
    last name limited to 20 char. If the handle is already taken then the user
    id (which is guaranteed to be unique) is appended to the handle keeping to
    the max 20 char limit.
    """
    # Create the user's handle from their first and last name
    handle_str = (name_first + name_last).lower()

    # Limit handle to maximum 20 char
    if len(handle_str) > 20:
        handle_str = handle_str[:20]

    # Check if handle is already taken
    for user in data.get_data().get_user_list():
        if handle_str == user.get_handle_str():

            # If the handle + u_id exceeds 20 char
            if len(handle_str + str(u_id)) > 20:
                handle_str = handle_str[:20 - len(str(u_id))] + str(u_id)

            # Else just append the u_id to the handle
            else:
                handle_str = handle_str + str(u_id)

            break

    return handle_str


def generate_hash(password):
    """
    The user's password on registration is hashed using the sha512 algorithm. It
    is also salted using a random generator from Python's secrets module.
    """
    # Creating a salt
    alphabet = string.ascii_letters + string.digits
    salt = ''.join(secrets.choice(alphabet) for i in range(16))

    # Salt the password and hash it
    pepper = hashlib.sha512((salt + password).encode()).hexdigest()

    return salt, pepper


def hash_it(salt, password):
    """
    Return the hash for a salt and password combination
    """
    return hashlib.sha512((salt + password).encode()).hexdigest()
