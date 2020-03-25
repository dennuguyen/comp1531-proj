<<<<<<< HEAD
"""
Data.py defines the classes used to store the server data in memory and methods
to get or manipulate that data. These classes are:
-> Login
-> Channel
-> User
-> React
-> Message
-> Password
-> Data

The Data class instantiates the parent object, data, which contains the lists of
child objects i.e. instantiations of the Login, Channel, User, Message, Password
classes. Each child object has getters and setters that respectively return and
manipulate their unique member variables.

The Data class has multiple getters which returns the list of objects or returns
an object depending on the nature of the getter and its given parameters.

    e.g. get_user_list()

         Returns the list of user objects.

    e.g. get_user_with_token(self, token) and get_user_with_u_id(self, u_id)

         Both return an instance of User from the list of user objects.

The purpose of retrieving the same object with different parameters allows
fellow programmers the flexibility to implement their source file functions
however they like.

The Data class also has adders to append child objects to the list of objects
and removers to remove child objects from the list of objects. This action
signifies the creation and deletion of those objects.

    e.g. add_user(self, new_user)

         Accepts a User object, new_user, and appends this to the list of users.
         This is called upon registration of a new user.
=======
<<<<<<< HEAD
'''
- Data related operation functions are here.
- Please read all of the functions below before you call one of them in your file.
- Currently, data is all stored in the program using a global object vairable.
- Functions may not be named in a way what you like so please just 'Ctrl + H' to 
change them to better ones.
- There should be some functions not coverd in this file and you can add whatever 
you want follow the structureor just inform me to help you add something you need.
- I don't have time to test all functions below and maybe there are some small 
mistakes but it's easy to correct them I believe.
- Setters are something to implement later.

'''
  
class Login():
    
    def __init__(self, u_id, token_list):
        self.u_id = u_id
        self.token_list = token_list
>>>>>>> dev2
    
    e.g. remove_user(self, user)

         Removes a User object, user, from the list of users.

The Data class also contains the "global" user id, channel id, and message id.
Data methods are called for use of these global ids as to get the global id
value as well as automate its incrementation (without programmer intervention).

The Data class has a reset method to conveniently reset server data in memory.
"""





################################################################################
# NOTICE for git-push-me-out-a-window:                                         #
#                                                                              #
# - Please read all of the functions below before you call one of them in your #
#   file.                                                                      #
#                                                                              #
# - There may be functions that are bugged as they have not been properly      #
#   tested.                                                                    #
#                                                                              #
# - message_wait_list may require some getters in Data                         #                                                                    #
#                                                                              #
# - Underscores before a variable name indicates that variable is private.     #
#                                                                              #
################################################################################






class Login():
    """
    Login class
    """
    def __init__(self, u_id, token):
        self._u_id = u_id
        self._token = token
    
    """
    Getters
    """
    def get_login_dict(self):
        return {
            'u_id' : self._u_id,
            'token' : self._token,
        }
    
    def get_u_id(self):
        return self._u_id

    def get_token(self):
        return self._token
    


class Channel():
    """
    Channel class
    """
    def __init__(self,
                 ch_id,
                 ch_name,
                 msg_id_list,
                 u_id_list,
                 owner_u_id_list,
                 is_private
                ):
        self._ch_id = ch_id
        self._ch_name = ch_name
        self._msg_id_list = msg_id_list
        self._u_id_list = u_id_list
        self._owner_u_id_list = owner_u_id_list
        self._is_private = is_private
    
    """
    Getters
    """
    def get_channel_dict(self):
        return {
            'channel_id' : self._ch_id,
            'name' : self._ch_name,
            'message_id_list' : self._msg_id_list,
            'u_id_list' : self._u_id_list,
            'owner_u_id_list' : self._owner_u_id_list,
            'is_private' : self._is_private,
        }

    def get_channel_name(self):
        return self._ch_name
    
    def get_channel_id(self):
        return self._ch_id
    
    def get_msg_id_list(self):
        return self._msg_id_list

    def get_u_id_list(self):
        return self._u_id_list

    def get_owner_u_id_list(self):
        return self._owner_u_id_list
    
    def get_is_private(self):
        return self._is_private
    
    """
    Setters
    """
    def add_new_member(self, u_id):
        self._u_id_list.append(u_id)
    
    def add_new_owner(self, u_id):
        self._owner_u_id_list.append(u_id)
    
    def remove_member(self, u_id):
        self._u_id_list.remove(u_id)
    
    def remove_owner(self, u_id):
        self._owner_u_id_list.remove(u_id)

    def add_new_message(self, msg_id):
        self._msg_id_list.append(msg_id)

    def remove_message(self, msg_id):
        self._msg_id_list.remove(msg_id)



class User():
    """
    User class
    """
    def __init__(self, u_id, email, name_first, name_last, handle_str):
        self._u_id = u_id
        self._email = email
        self._name_first = name_first
        self._name_last = name_last
        self._handle_str = handle_str
    
    """
    Getters
    """
    def get_user_dict(self):
        return {
            'u_id' : self._u_id,
            'email' : self._email,
            'name_first' : self._name_first,
            'name_last' : self._name_last,
            'handle_str' : self._handle_str,
        }
    
    def get_member_details_dict(self):
        return {
            'u_id' : self._u_id,
            'name_first' : self._name_first,
            'name_last' : self._name_last,
        }

    def get_u_id(self):
        return self._u_id

    def get_email(self):
        return self._email

    def get_name_first(self):
        return self._name_first
    
    def get_name_last(self):
        return self._name_last

    def get_handle_str(self):
        return self._handle_str

    
    """
    Setters
    """
    def set_email(self, new_email):
        self._email = new_email

    def set_name_first(self, new_name_first):
        self._name_first = new_name_first
    
    def set_name_last(self, new_name_last):
        self._name_last = new_name_last

    def set_handle_str(self, new_handle_str):
        self._handle_str = new_handle_str


class React():
    """
    React Class
    """
    def __init__(self, react_id=-1, u_id_list=[], is_this_user_reacted=False):
        self._react_id = react_id
        self._u_id_list = u_id_list
        self._is_this_user_reacted = is_this_user_reacted
    
    """
    Getters
    """
    def get_react_dict(self):
        return {
            'react_id' : self._react_id,
            'u_ids' : self._u_id_list,
            'is_this_user_reacted' : self._is_this_user_reacted,
        }
    
    def get_react_id(self):
        return self._react_id

    def get_u_id_list(self):
        return self._u_id_list
    
    def get_is_this_user_reacted(self):
        return self._is_this_user_reacted
    
    """
    Setters
    """
    def add_u_id(self, u_id):
        self._u_id_list.append(u_id)

    def remove_u_id(self, u_id):
        self._u_id_list.remove(u_id)
    
    def set_is_this_user_reacted(self, flag):
        self._is_this_user_reacted = flag


class Message():
    """
    Message Class
    """
    def __init__(self,
                 msg_id,
                 u_id,
                 msg,
                 time_created,
                 react_list=[React(-1,[],False)],
                 is_pinned=False,
                ):
        self._msg_id = msg_id
        self._u_id = u_id
        self._msg = msg
        self._time_created = time_created
        self._react_list = react_list
        self._is_pinned = is_pinned
    
    """
    Getters
    """
    def get_message_dict(self):
        return {
            'message_id' : self._msg_id,
            'u_id' : self._u_id,
            'message' : self._msg,
            'time_created' : self._time_created,
            'reacts' : self._react_list,
            'is_pinned' : self._is_pinned,
        }
    
    def get_message_id(self):
        return self._msg_id

    def get_u_id(self):
        return self._u_id
    
    def get_message(self):
        return self._msg
    
    def get_time_created(self):
        return self._time_created
    
    def get_react_list(self):
        return self._react_list

    def get_react_with_react_id(self, react_id):
        for react in react_list:
            if(react_id == react.get_react_id()):
                return react.get_react_dict()
        
        return None
    
    def get_is_pinned(self):
        return self._is_pinned

    """
    Setters
    """
    def set_message(self, new_msg):
        self._msg = new_msg
    
    def set_time_created(self, new_time_created):
        self._time_created = new_time_created

    def set_react(self, react_id, u_id, flag):  # Need to make sure this works, cannot tell by looking
        for react in self._react_list:
            if (react.get_react_id() == react_id):
                react.set_is_this_user_reacted(flag)
                react.add_u_id(u_id)              
                break
    
    def set_is_pinned(self, flag):
        self._is_pinned = flag


class Password():
    """
    Password class
    """
    def __init__(self, u_id, salt, hash_):
        self._u_id = u_id
        self._salt = salt
        self._hash = hash_

    """
    Getters
    """
    def get_u_id(self):
        return self._u_id
    
    def get_salt(self):
        return self._salt
    
    def get_hash(self):
        return self._hash

    """
    Setters
    """
    def set_u_id(self, new_u_id):
        self._u_id = new_u_id
    
    def set_salt(self, new_salt):
        self._salt = new_salt
    
    def set_hash(self, new_hash):
        self._hash = new_hash

class Data():
    """
    Data class
    """
    def __init__(self,
                 user_list=[],
                 message_list=[],
                 message_wait_list=[],
                 channel_list=[],
                 login_list=[],
                 password_list=[],
                 u_id=-1,
                 ch_id=-1,
                 msg_id=-1
                ):
        self._user_list = user_list
        self._message_list = message_list
        self._message_wait_list = message_wait_list
        self._channel_list = channel_list
        self._login_list = login_list
        self._password_list = password_list
        """
        Global (but not really) variables to keep track of the id's of users,
        channels, messages.
        """
        self._u_id = u_id
        self._ch_id = ch_id
        self._msg_id = msg_id

    """
    Getters
    """
    def get_user_list(self):
        return self._user_list

    def get_message_list(self):
        return self._message_list
    
    def get_channel_list(self):
        return self._channel_list

    def get_login_list(self):
        return self._login_list

    def get_password_list(self):
        return self._password_list

    # def get_all_user_id(self):
    #     return [user.get_u_id() for user in self._user_list]

    # def get_all_message_id(self):
    #     return [message.get_message_id() for message in self._message_list]

    # def get_all_channel_id(self):
    #     return [channel.get_channel_id() for channel in self._channel_list]

    # def get_all_channel_names(self):
    #     return [channel.get_channel_name() for channel in self._channel_list]
    
    # def get_all_login_id(self):
    #     return [login.get_u_id() for login in self._login_list]

    """
    User Object Getters
    """
    def get_user_with_u_id(self, u_id):
        for user in self._user_list:
            if (user.get_u_id() == u_id):
                return user

        return None

    def get_user_with_token(self, token):
        for user in self._user_list:
            if (user.get_token() == token):
                return user

        return None

    def get_user_with_email(self, email):
        for user in self._user_list:
            if (user.get_email() == email):
                return user

        return None

    def get_user_with_handle_str(self, handle_str):
        for user in self._user_list:
            if (user.get_handle_str() == handle_str):
                return user

        return None

    """
    Channel Object Getters
    """
    def get_channel_with_ch_id(self, ch_id):
        for channel in self._channel_list:
            if (channel.get_channel_id() == ch_id):
                return channel

        return None

    def get_channel_with_message_id(self, msg_id):
        for channel in self._channel_list:
            if (channel.get_channel_id())

        return None

    """
    Login Object Getters
    """
    def get_login_with_u_id(self, u_id):  
        return [login for login in self._login_list if login.get_u_id() == u_id]

    def get_login_with_token(self, token):
        for login in self._login_list:
            if (login.get_token() == token):
                return login

        return None

    """
    React Object Getters
    """
    def get_react_with_react_id(self, react_id):  
        for react in self._react_list:
            if (react.get_react_id() == react_id):
                return react

        return None

    """
    Message Object Getters
    """
    def get_message_with_message_id(self, msg_id):
        for msg in self._message_list:
            if (msg.get_message_id() == msg_id):
                return msg
            
        return None

    def get_message_with_u_id(self, u_id):
        # A user may send multiple messages
        return [msg for msg in self._message_list if msg.get_u_id() == u_id]

    def get_message_with_message(self, message)
        return [msg for msg in self._message_list if msg.get_message() == message]

    """
    Password Object Getters
    """
    def get_password_with_u_id(self, u_id):
        for pass_ in self._password_list:
            if pass_.get_u_id() == u_id:
                return pass_
        
        return None
    
    def get_password_with_salt(self, salt):
        for pass_ in self._password_list:
            if pass_.get_salt() == salt:
                return pass_
        
        return None

    def get_password_with_hash(self, hash_):
        for pass_ in self._password_list:
            if pass_.get_hash() == hash_:
                return pass_
        
        return None

    """
    Adders

    Adds objects to their respective list of objects
    """
    def add_user(self, new_user):
        try:
            assert isinstance(new_user, User)
            self._user_list.append(new_user)
        except AssertionError:
            raise AssertionError("Error: Parameter is not 'class User'")

    def add_message(self, new_message):
        try:
            assert isinstance(new_message, Message)
            self._message_list.append(new_message)
        except AssertionError:
            raise AssertionError("Error: Parameter is not 'class Message'")

    def add_channel(self, new_channel):
        try:
            assert isinstance(new_channel, Channel)
            self._channel_list.append(new_channel)
        except AssertionError:
            raise AssertionError("Error: Parameter is not 'class Channel'")

    def add_login(self, new_login):
        try:
            assert isinstance(new_login, Login)
            self._login_list(new_login)
        except AssertionError:
            raise AssertionError("Error: Parameter is not 'class Login'")

<<<<<<< HEAD
    def add_message_later(self, new_message):
        try:
            assert isinstance(new_message, Message)
            self._message_wait_list.append(new_message)
        except AssertionError:
            raise AssertionError("Error: Parameter is not 'class Message'")
    # def add_message_later(self, msg_id):
    #     msg = self._get_message_with_message_id(msg_id)
    #     self._message_wait_list.append(msg)

    """
    Removers

    Removes objects from their respective list of objects
    """
    def remove_user(self, user):
        try:
            assert isinstance(user, User)
            self._user_list.remove(user)
        except AssertionError:
            raise AssertionError("Error: Parameter is not 'class User'")

    def remove_message(self, message):
        try:
            assert isinstancemessage, Message)
            self._message_list.remove(message)
        except AssertionError:
            raise AssertionError("Error: Parameter is not 'class Message'")

    def remove_channel(self, channel):
        try:
            assert isinstance(channel, Channel)
            self._channel_list.remove(channel)
        except AssertionError:
            raise AssertionError("Error: Parameter is not 'class Channel'")

    def remove_login(self, login):
        try:
            assert isinstance(login, Login)
            self._login_list.remove(login)
        except AssertionError:
            raise AssertionError("Error: Parameter is not 'class Login'")

    def remove_message_later(self, message):
        try:
            assert isinstancemessage, Message)
            self._message_wait_list.remove(message)
        except AssertionError:
            raise AssertionError("Error: Parameter is not 'class Message'")
    # def remove_message_later(self, msg_id):
    #         msg = self._get_message_with_message_id(msg_id)
    #         self._message_wait_list.remove(msg)

    """
    Incrementers
    """
    def global_u_id(self):
        self._u_id += 1
        return self._u_id
    
    def global_ch_id(self):
        self._ch_id += 1
        return self._ch_id
    
    def global_msg_id(self):
        self._msg_id += 1
        return self._msg_id

    # """
    # Calling these classes will return the (global) variable
    # and increment it automatically.

    # e.g. my_id = get_data().global_u_id()
    # """
    # class global_u_id():
    #     id = -1
    #     def __new__(cls):
    #         cls.id += 1
    #         return cls.id
    
    # class global_ch_id():
    #     id = -1
    #     def __new__(cls):
    #         cls.id += 1
    #         return cls.id
    
    # class global_msg_id():
    #     id = -1
    #     def __new__(cls):
    #         cls.id += 1
    #         return cls.id
    
    """
    Resets the data state
    """
    def reset(self):
        self._user_list = []
        self._message_list = []
        self._channel_list = []
        self._member_list = []
        self._login_list = []
        
        self._next_u_id = -1
        self._next_channel_id = -1
        self._next_message_id = -1
        
"""
Instantiate data from Data
"""
data = Data()

def get_data():
    """
    get_data() allows loose coupling between the possibility of permanating
    Data and the Data implementation
    """
    global data   
    return data
=======
    # get the user_dict with u_id
user_dict = getData().get_user_dict(u_id)
print(user_dict)
'''
=======
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
            'email': 0,
            'name_first': 0,
            'name_last': 0,
            'handle_str': 0,
        },
    ],
    # Stores messages including details
    'messages': [
        {
            'message_id': 0,
            'u_id': 0,
            'message': 0,
            'time_created': 0,
        },
    ],
    # Stores channels including details
    'channels': [
        {
            'channel_id': 0,
            'name': 0,
            'isprivate': 0,
            'owner_members': [
                {
                    'u_id': 0,
                    'name_first': 0,
                    'name_last': 0,
                },
            ],
            'name_last': [
                {
                    'u_id': 0,
                    'name_first': 0,
                    'name_last': 0,
                },
            ],
        },
    ],
    'passwords': [
        {
            'salt': 0,
            'hash': 0,
            'email': 0,
        },
    ]
}

with open("data.json", "w+") as f:
    json.dump(data, f)
>>>>>>> it2_decorators
>>>>>>> dev2
