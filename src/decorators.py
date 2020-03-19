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
