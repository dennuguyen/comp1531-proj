#Message_send

def send(token, channel_id, message):
    return {
        'message_id': 1,
    }

#Message_remove

def remove(token, message_id):
    return {
    }

#Message_edit

def edit(token, message_id, message):
    return {
    }

#General_functions

def check_token_is_valid(token):
    return True

def check_channel_id_is_valid(channel_id):
    return True

def check_user_is_member(token, channel_id):
    return True

def check_message_is_valid(message):
    return False

def check_message_id_is_valid(message_id):
    return True

def check_if_authorised_user(token, message_id):
    return True






