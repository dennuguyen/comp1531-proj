import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth
import user


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


@APP.route('/login', methods=['GET', 'POST'])
# Get the email and password from page for login
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth.auth_login(email, password)

    return


@APP.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # get the user info
        email = request.form['email']
        password = request.form['password']
        name_first = request.form['name_first']
        name_last = request.form['name_last']

        # register the user
        auth.auth_register(email, password, name_first, name_last)

    elif request.method == 'GET':
        # request.args.get('name')
        pass


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
