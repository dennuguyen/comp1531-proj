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

    return json.dumps(user.user_profile(token, u_id))

# @APP.route("/user/profile/setname", methods=["PUT"])
# @APP.route("/user/profile/setemail", methods=["PUT"])
# @APP.route("/user/profile/sethandle", methods=["PUT"])
# @APP.route("/users/all", methods=["GET"])
# @APP.route("/search", methods=["GET"])
# @APP.route("/standup/start", methods=["POST"])
# @APP.route("/standup/active", methods=["GET"])
# @APP.route("/standup/send", methods=["POST"])
# @APP.route("/admin/userpermission/change", methods=["POST"])
# @APP.route("/workspace/reset", methods=["POST"])
# def reset():
#     try:

# This will run if server.py is run
if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080),
            debug=True)
