import json


class Data():
    def pickle():
        pass

    def unpickle():
        pass


# Users class inherits Data's pickle and unpickle methods
# Users class stores registered users and methods to edit the data structure
class Users(Data):
    # Class constructor for new initial user
    # No need to declare the users data structure in Python
    def __init__(self):
        self.users = [
            {
                'u_id': 0,
                'email': '',
                'name_first': '',
                'name_last': '',
                'handle_str': '',
            },
        ]

    # Member functions
    # Must pass self as parameter if methods of class act on itself
    def get_users(self):
        return self.users

    def add_user(self, user):
        self.users.append(user)


data = {
    # Stores logged in users
    'login': [
        {
            'u_id': 0,
            'token': 0,
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