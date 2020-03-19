import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth
import user
import error


#
def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        'code': err.code,
        'name': 'System Error',
        'message': err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)  # Create an instance APP from the Flask class
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


# Example - echo page
@APP.route('/echo', methods=['GET'])
#
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({'data': data})


# Register
@APP.route('/register', methods=['POST'])
def register():
    while True:
        try:
            if request.method == 'POST':
                # Get the user information
                register_retval = request.get_json()
                email = register_retval['email']
                password = register_retval['password']
                name_first = register_retval['name_first']
                name_last = register_retval['name_last']

                # Perform the user registration
                auth.auth_register(
                    email=email,
                    password=password,
                    name_first=name_first,
                    name_last=name_last,
                )

        except error.InputError:
            pass

        except Exception:
            print("GOt an exception here")

        else:
            break


# Login the user
@APP.route('/login', methods=['POST'])
def login():
    while True:
        try:
            if request.method == 'POST':
                # Get the login information
                login_retval = request.get_json()
                email = login_retval['email']
                password = login_retval['password']

                # Perform the login
                auth.auth_login(
                    email=email,
                    password=password,
                )

        except error.InputError:
            pass

        except Exception:
            print("GOt an exception here")

        else:
            break


@APP.route('/profile', methods=['GET'])
# Get token and u_id from ___
def get_profile():
    # try:
    # token = request.form['token']
    # u_id = request.form['u_id']
    # return user.user_profile(token, u_id)
    #     pass
    # except:
    pass


# This will run if server.py is run
if __name__ == '__main__':
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
