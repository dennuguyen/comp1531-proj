import data
import decorators
import auth_helper


@decorators.authenticate_email
@decorators.authenticate_password
def auth_login(*, email, password):

    # Find the matching email and password in the database
    for user in data.data['users']:
        if email == user['email']:
            if password == user['password']:
                return {
                    'u_id': user['u_id'],
                    'token': auth_helper.generate_token(email),
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
    new_user['handle_str'] = auth_helper.generate_handle(
        new_user['u_id'], name_first, name_last)

    # Add the registered user's information to the database
    data.data['users'].append(new_user)

    # Generate the hashed password for the new user
    auth_helper.generate_hash(email, password)

    # Return the registered user's u_id and their session token
    return {
        'u_id': new_user['u_id'],
        'token': auth_helper.generate_token(new_user['u_id']),
    }
