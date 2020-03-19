def authenticate_token(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Assert the number of arguments is greater than 1
        # assert args >= 1

        # Get the token
        token = kwargs['token'])
        # Assert the token
        assert token == 1

        return fn(*args, **kwargs)

    return wrapper

def authenticate_email(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the email
        email = kwargs['email'])
        print(email)

        return fn(*args, **kwargs)

    return wrapper

def authenticate_password(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):

        # Get the password
        password = kwargs['password'])
        print(password)

        return fn(*args, **kwargs)

    return wrapper