import data
import decorators
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


@decorators.authenticate_email
@decorators.authenticate_password
def auth_login(*, email, password):

    # Find the matching email and password in the database
    for user in data.data['users']:
        if email == user['email']:
            if password == user['password']:
                return {
                    'u_id': user['u_id'],
                    'token': generate_token(email),
                }

    # Retrieve the salt by looking up the email in the passwords data structure

    # Does the user know their password


@decorators.authenticate_token
def auth_logout(*, token):

    # Successful logout is false
    is_true = False

    # Search for matching token
    for i in range(len(data.data['login'])):
        # Invalidate the token
        if data.data['login'][i].get('token') == token:
            is_true = True
            del data.data['login'][i]
            break

    return {'is_success': is_true}


@decorators.authenticate_email
@decorators.register_email
@decorators.authenticate_password
@decorators.authenticate_name_first
@decorators.authenticate_name_last
def auth_register(*, email, password, name_first, name_last):

    # Get the information for the new user
    new_user = {}
    new_user['u_id'] = data.data['users'][-1]['u_id'] + 1
    new_user['email'] = email
    new_user['name_first'] = name_first
    new_user['name_last'] = name_last
    new_user['handle_str'] = generate_handle(new_user['u_id'], name_first,
                                             name_last)

    # Add the registered user's information to the database
    data.data['users'].append(new_user)

    # Generate the hashed password for the new user
    generate_hash(email, password)

    # Return the registered user's u_id and their session token
    return {
        'u_id': new_user['u_id'],
        'token': generate_token(new_user['u_id']),
    }
