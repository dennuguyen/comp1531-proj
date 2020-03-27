"""
Server.py handles the server routing.

Body Content Type: application/json
GET requests: query string
POST requests: JSON object
"""
import sys
import json
import flask
import flask_cors
import error
import auth
import channel
import channels
import message
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
    Echo example page.
    """
    data = flask.request.args.get("data")
    if data == "echo":
        raise error.InputError(description="Cannot echo \"echo\"")
    return json.dumps({"data": data})


@APP.route("/auth/login", methods=["POST"])
def auth_login():
    """
    Login gets an email and password and passes them to auth_login.
    """
    # Get the login information
    retval = flask.request.get_json()
    email = retval["email"]
    password = retval["password"]

    # Perform the login
    return auth.auth_login(email=email, password=password)


@APP.route("/auth/logout", methods=["POST"])
def auth_logout():
    """
    Logout gets the token and passes the token to auth_logout.
    """
    # Log the user out with token from the query string
    token = flask.request.get_json()['token']
    return auth.auth_logout(token=token)

    # Redirect the user to the login page
    # return flask.redirect(flask.url_for('login'))


@APP.route("/auth/register", methods=["POST"])
def auth_register():
    """
    Register gets an email, password and name and passes them to auth_register.
    """
    # Get the register information
    retval = flask.request.get_json()
    email = retval["email"]
    password = retval["password"]
    name_first = retval["name_first"]
    name_last = retval["name_last"]

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
    Invite gets the token, channel id, and user id and passes them to
    channel_invite.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    channel_id = retval["channel_id"]
    u_id = retval["u_id"]
    return channel.channel_invite(token=token,
                                  channel_id=channel_id,
                                  u_id=u_id)


@APP.route("/channel/details", methods=["POST"])
def channel_details():
    """
    Channel details gets a token and channel id and passes them to
    channel_details.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    channel_id = retval["channel_id"]
    return channel.channel_details(token=token, channel_id=channel_id)


@APP.route("/channel/messages", methods=["GET"])
def channel_messages():
    """
    Channel messages gets a token, channel id and message start index and
    passes it to channel_messages.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    channel_id = retval["channel_id"]
    start = retval["start"]
    return channel.channel_messages(token=token,
                                    channel_id=channel_id,
                                    start=start)


@APP.route("/channel/leave", methods=["POST"])
def channel_leave():
    """
    Channel leave gets a token and channel id and passes it to channel_messages.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    channel_id = retval["channel_id"]
    return channel.channel_leave(token=token, channel_id=channel_id)


@APP.route("/channel/join", methods=["POST"])
def channel_join():
    """
    Channel join gets a token and channel id and passes it to channel_join.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    channel_id = retval["channel_id"]
    return channel.channel_join(token=token, channel_id=channel_id)


@APP.route("/channel/addowner", methods=["POST"])
def channel_addowner():
    """
    Channel add owner gets a token, channel id, and user id and passes it to
    channel_addowner.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    channel_id = retval["channel_id"]
    u_id = retval["u_id"]
    return channel.channel_addowner(token=token,
                                    channel_id=channel_id,
                                    u_id=u_id)


@APP.route("/channel/removeowner", methods=["POST"])
def channel_removeowner():
    """
    Channel remove owner gets a token, channel id, and user id and passes it to
    channel_removeowner.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    channel_id = retval["channel_id"]
    u_id = retval["u_id"]
    return channel.channel_removeowner(token=token,
                                       channel_id=channel_id,
                                       u_id=u_id)


@APP.route("/channels/list", methods=["GET"])
def channels_list():
    """
    Channels list takes a token and passes it to channels_list.
    """
    token = flask.request.args.get("token")
    return channels.channels_list(token=token)


@APP.route("/channels/listall", methods=["GET"])
def channels_listall():
    """
    Channels listall takes a token and passes it to channels_listall.
    """
    token = flask.request.args.get("token")
    return channels.channels_listall(token=token)


@APP.route("/channels/create", methods=["POST"])
def channels_create():
    """
    Channels create takes a token, channel name and is_public boolean and
    passes it to channels_create.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    name = retval["name"]
    is_public = retval["is_public"]
    return channels.channels_create(token=token,
                                    name=name,
                                    is_public=is_public)


@APP.route("/message/send", methods=["POST"])
def message_send():
    """
    Message send takes a token, channel id and message and passes it to
    message_send.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    channel_id = retval["channel_id"]
    message_ = retval["message"]
    return message.message_send(token=token,
                                channel_id=channel_id,
                                message=message_)


@APP.route("/message/sendlater", methods=["POST"])
def message_sendlater():
    """
    Message sendlater takes a token, channel id and message and passes it to
    message_send.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    channel_id = retval["channel_id"]
    message_ = retval["message"]
    time_sent = retval["time_sent"]
    return message.message_sendlater(token=token,
                                     channel_id=channel_id,
                                     message=message_,
                                     time_sent=time_sent)


@APP.route("/message/react", methods=["POST"])
def message_react():
    """
    Message react takes a token, message id and react id and passes it to
    message_react.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    message_id = retval["message_id"]
    react_id = retval["react_id"]
    return message.message_react(token=token,
                                 message_id=message_id,
                                 react_id=react_id)


@APP.route("/message/unreact", methods=["POST"])
def message_unreact():
    """
    Message unreact takes a token, message id and react id and passes it to
    message_unreact.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    message_id = retval["message_id"]
    react_id = retval["react_id"]
    return message.message_unreact(token=token,
                                   message_id=message_id,
                                   react_id=react_id)


@APP.route("/message/pin", methods=["POST"])
def message_pin():
    """
    Message pin takes a token, and message id and passes it to
    message_pin.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    message_id = retval["message_id"]
    return message.message_pin(token=token, message_id=message_id)


@APP.route("/message/unpin", methods=["POST"])
def message_unpin():
    """
    Message unpin takes a token, and message id and passes it to
    message_unpin.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    message_id = retval["message_id"]
    return message.message_unpin(token=token, message_id=message_id)


@APP.route("/message/remove", methods=["DELETE"])
def message_remove():
    """
    Message remove takes a token, and message id and passes it to
    message_remove.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    message_id = retval["message_id"]
    return message.message_remove(token=token, message_id=message_id)


@APP.route("/message/edit", methods=["PUT"])
def message_edit():
    """
    Message edit takes a token, message id, and message and passes it to
    message_edit.
    """
    retval = flask.request.get_json()
    token = retval["token"]
    message_id = retval["message_id"]
    message_ = retval["message"]
    return message.message_edit(token=token,
                                message_id=message_id,
                                message=message_)


################################################################################

# @APP.route("/user/profile", methods=["GET"])
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
