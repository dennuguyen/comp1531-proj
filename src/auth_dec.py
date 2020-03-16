import error
import user
import re


# Check if email has valid form
def check_valid_email(email):

    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if not re.search(regex, email):
        raise error.InputError('Invalid email.')
    else:
        pass


# Check if email already exists, if so raise InputError
def check_existing_email(email):
    for user in user.users:
        if email == user['email']:
            raise error.InputError('Email already exists.')


# raise InputError when wrong password, invalid email
def authenticate_login(fn, *args, **kwargs):

    print('Logging in...')

    def wrapper(email, password, *args, **kwargs):
        # Authenticate the email
        check_valid_email(email)
        check_existing_email(email)
        return fn(email, password, *args, **kwargs)

    return wrapper


def authenticate_logout(fn, *args, **kwargs):

    print('Logging out...')

    def wrapper(email, password, *args, **kwargs):
        # do stuff
        try:
            return fn(email, password, *args, **kwargs)
        except:
            raise error.InputError

    return wrapper


def authenticate_register(fn, *args, **kwargs):

    print('Registering...')

    def wrapper(email, password, *args, **kwargs):
        # do stuff
        try:
            return fn(email, password, *args, **kwargs)
        except:
            raise error.InputError

    return wrapper
