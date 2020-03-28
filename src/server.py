"""
Server.py handles the server routing.

GET requests:
- Parameters are URL arguments
- request.args.get()

POST requests:
- Parameters are JSON object in body of request
- request.get_json() for POST requests
- Parameters are URL arguments
- request.args.get()

DELETE requests:
- 
- 
"""
import sys
import json
import flask
import flask_cors
import error
import auth
import channel
import user
import admin


def defaultHandler(err):
    response = err.get_response()
    print("response", err, err.get_response())
    response.data = json.dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = "application/json"
    return response


APP = flask.Flask(__name__)
flask_cors.CORS(APP)
APP.config["TRAP_HTTP_EXCEPTIONS"] = True
APP.register_error_handler(Exception, defaultHandler)


@APP.route("/echo", methods=["GET"])
def echo():
    """
    Echo example page
    """
    data = flask.request.args.get("data")
    if data == "echo":
        raise error.InputError(description="Cannot echo \"echo\"")
    return json.dumps({"data": data})


@APP.route("/auth/login", methods=["POST"])
def login():
    """
    Login gets an email and password from a POST request and passes them to
    auth_login.
    """
    # Get the login information
    req = flask.request.get_json()
    email = req["email"]
    password = req["password"]

    # Perform the login
    return auth.auth_login(email=email, password=password)


@APP.route("/auth/logout", methods=["POST"])
def logout():
    """
    Logout gets the token from the query string and passes the token to
    auth_logout. The user is then redirected to the login page.
    """
    # Log the user out with token from the query string
    token = flask.request.args.get('token')
    assert auth.auth_logout(token=token)

    # Redirect the user to the login page
    return flask.redirect(flask.url_for('login'))


@APP.route("/auth/register", methods=["POST"])
def register():
    """
    Register gets an email, password and name from a POST request and passes
    them to auth_register
    """
    # Get the register information
    req = flask.request.get_json()
    email = req["email"]
    password = req["password"]
    name_first = req["name_first"]
    name_last = req["name_last"]

    # Perform the user registration
    return auth.auth_register(
        email=email,
        password=password,
        name_first=name_first,
        name_last=name_last,
    )


@APP.route("/channel/invite", methods=["POST"])
def channel_invite():
    """
    Invite gets the token, channel id and user id from the query string
    and passes them to channel_invite.
    """
    token = flask.request.args.get("token")
    ch_id = flask.request.args.get("channel_id")
    u_id = flask.request.args.get("u_id")
    return channel.channel_invite(token=token, channel_id=ch_id, u_id=u_id)


@APP.route("/channel/details", methods=["GET"])
def channel_details():
    """
    Channel invite page
    """
    return channel.channel_details(token=1, channel_id=1)


# @APP.route("/channel/messages", methods=["GET"])
# @APP.route("/channel/leave", methods=["POST"])
# @APP.route("/channel/join", methods=["POST"])
# @APP.route("/channel/addowner", methods=["POST"])
# @APP.route("/channel/removeowner", methods=["POST"])
# @APP.route("/channels/list", methods=["GET"])
# @APP.route("/channels/listall", methods=["GET"])
# @APP.route("/channels/create", methods=["POST"])
# @APP.route("/message/send", methods=["POST"])
# @APP.route("/message/sendlater", methods=["POST"])
# @APP.route("/message/react", methods=["POST"])
# @APP.route("/message/unreact", methods=["POST"])
# @APP.route("/message/pin", methods=["POST"])
# @APP.route("/message/unpin", methods=["POST"])
# @APP.route("/message/remove", methods=["DELETE"])
# @APP.route("/message/edit", methods=["PUT"])

################################################################################

@APP.route("/user/profile", methods=["GET"])
def user_profile():
    '''
    Get the information of a user
    '''
    token = flask.request.args.get("token")
    u_id = flask.request.args.get("u_id")

    return user.user_profile(token=token, u_id=u_id)

@APP.route("/user/profile/setname", methods=["PUT"])
def user_profile_setname():
    '''
    Set the name of a user
    '''
    token = flask.request.form.get('token')
    name_first = flask.request.form.get('name_first')
    name_last = flask.request.form.get('name_last')

    return user.user_profile(token=token, name_first=name_first, name_last=name_last)

@APP.route("/user/profile/setemail", methods=["PUT"])
def user_profile_setmail():
    '''
    Set the email of a user
    '''
    token = flask.request.form.get('token')
    email = flask.request.form.get('email')

    return user.user_profile_setemail(token=token, email=email)

@APP.route("/user/profile/sethandle", methods=["PUT"])
def user_profile_sethandle():
    '''
    Set the handle of a user
    '''
    token = flask.request.form.get('token')
    handle = flask.request.handle.get('handle')

    return user.user_profile_sethandle(token=token, handle=handle)

@APP.route("/users/all", methods=["GET"])
def users_all():
    '''
    Get all the users
    '''
    token = flask.request.args.get('token')

    return other.user_all(token=token)

@APP.route("/search", methods=["GET"])
def search():
    '''
    Search for the exsiting messages
    '''
    query_str = flask.request.args.get('query_str')

    return other.search(query_str=query_str)

@APP.route("/standup/start", methods=["POST"])
def standup_start():
    '''
    Start a standup
    '''
    token = flask.request.form.get('token')
    channel_id = flask.request.form.get('channel_id')
    length = flask.request.form.get('length')

    return standup.stanup_start(token=token, channel_id=channel_id, length=length)

@APP.route("/standup/active", methods=["GET"])
def standup_active():
    '''
    Set the standup active
    '''
    token = flask.request.args.get('token')
    channel_id = flask.request.args.get('channel_id')

    return standup.standup_active(token=token, channel_id=channel_id)

@APP.route("/standup/send", methods=["POST"])
def standup_send():
    '''
    Send the standup message
    '''
    token = flask.request.form.get('token')
    channel_id = flask.request.form.get('channel_id')
    message = flask.request.form.get('message')

    return standup.standup_send(token=token, channel_id=channel_id, message=message)

@APP.route("/admin/userpermission/change", methods=["POST"])
def admin_userpermission_change():
    '''
    Change the permission of users by the admin
    '''
    token = flask.request.form.get('token')
    u_id = flask.request.form.get('u_id')
    permission_id = flask.request.form.get('permission_id')

    return admin.admin_userpermission_change(token=token, u_id=u_id, permission_id=permission_id)


@APP.route("/workspace/reset", methods=["POST"])
def reset():
    '''
    Reset the workspace
    '''
    try:

#This will run if server.py is run
if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080),
            debug=True)
