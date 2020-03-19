import re
import error
import user


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

        # 
        for user in user.users:
        if email == user['email']:
            raise error.InputError('Email already exists.')
        else:
            pass

        return fn(*args, **kwargs)

    return wrapper


def authenticate_password(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the password
        password = kwargs['password']
        print(password)

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