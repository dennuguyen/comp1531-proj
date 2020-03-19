import decorators


@decorators.authenticate_token
@decorators.authenticate_u_id
def user_profile(*, token, u_id):

    print('Hello\n')

    return {
        'user': {
            'u_id': u_id,
            'email': email,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': handle_str,
        },
    }


@decorators.authenticate_token
@decorators.authenticate_name_first
@decorators.authenticate_name_last
def user_profile_setname(token, name_first, name_last):

    return {}


@decorators.authenticate_token
@decorators.authenticate_email
def user_profile_setemail(token, email):
    return {}


@decorators.authenticate_token
@decorators.authenticate_handle_str
def user_profile_sethandle(token, handle_str):
    return {}


user_profile(token='token', u_id=3)
