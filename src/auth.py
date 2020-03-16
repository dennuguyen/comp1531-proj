import auth_dec


@auth_dec.authenticate_login
def auth_login(email, password):

    u_id = 1
    token = 1

    return {
        'u_id': u_id,
        'token': token,
    }


@auth_dec.authenticate_logout
def auth_logout(token):
    return {
        'is_success': True,
    }


@auth_dec.authenticate_register
def auth_register(email, password, name_first, name_last):
    return {
        'u_id': 1,
        'token': '12345',
    }
