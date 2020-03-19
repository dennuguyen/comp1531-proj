import data
import hashlib
import string
import secrets

# temporary hard-to-guess url containing a security token for password recovery
# url = 'https://mydomain.com/reset=' + secrets.token_urlsafe()


# The token is generated using token_hex() from Python's secrets module.
#
# The generated token and the accompanying u_id will automatically be added to
# the logged in users database.
def generate_token(u_id):
    # Generate a token
    token = secrets.token_hex()

    # Create a login dictionary
    new_log = {'u_id': u_id, 'token': token}

    # Store the token in a database to keep track of logged in users
    data.data['login'].append(new_log)


# The handle is the concatentation of the lower case of the first name and last
# name limited to 20 char.
#
# If the handle is already taken then the user id (which is guaranteed to be
# unique) is appended to the handle keeping to the max 20 char limit.
def generate_handle(u_id, name_first, name_last):
    # Create the user's handle from their first and last name
    handle_str = (name_first + name_last).lower()

    # Limit handle to maximum 20 char
    if len(handle_str) > 20:
        handle_str = handle_str[:20]

    # Check if handle is already taken
    for user in data.data['users']:
        if handle_str == user['handle_str']:

            # If the handle + u_id exceeds 20 char
            if len(handle_str + str(u_id)) > 20:
                handle_str = handle_str[:20 - len(str(u_id))] + str(u_id)

            # Else just append the u_id to the handle
            else:
                handle_str = handle_str + str(u_id)

            break

    return handle_str


# The user's password on registration is hashed using the sha512 algorithm. It
# is also salted using a random generator from Python's secrets module.
#
# The salt, hash and email of the user is stored in a passwords database for
# lookup when the user relogs in.
def generate_hash(email, password):
    # Creating a salt
    alphabet = string.ascii_letters + string.digits
    salt = ''.join(secrets.choice(alphabet) for i in range(16))

    # Salt the password and hash it
    pepper = hashlib.sha512((salt + password).encode()).hexdigest()

    # Store the salt, hash and username
    data_entry = {salt, pepper, email}
    data.data['passwords'].append(data_entry)

    return pepper