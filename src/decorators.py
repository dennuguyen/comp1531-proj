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