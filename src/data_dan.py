import json

data = {
    # Stores logged in users
    'login': [
        {
            'u_id': 0,
            'token': 0,
        },
    ],
    # Stores registered users
    'users': [
        {
            'u_id': 0,
            'email': '',
            'name_first': '',
            'name_last': '',
            'handle_str': '',
        },
    ],
    # Stores messages including details
    'messages': [
        {
            'message_id': 0,
            'u_id': 0,
            'message': '',
            'time_created': 0,
            'reacts': [],
            'is_pinned': False
        },
    ],
    # Stores channels including details
    'channels': [
        {
            'channel_id': 0,
            'name': '',
            'message_id_list': [],
        },
    ],
    'members': [
        {
            'u_id': 0,
            'name_first': '',
            'name_last': '',
        },
    ],
    'reacts': [
        {
            'react_id': 0,
            'u_ids': [],
            'is_this_user_reacted': False,
        },
    ],
    'passwords': [
        {
            'salt': '',
            'hash': '',
            'email': '',
        },
    ]
}

with open("data.json", "w+") as f:
    json.dump(data, f)