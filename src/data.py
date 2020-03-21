<<<<<<< HEAD
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
=======
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
    
    def get_login_dict(self):
        return {
            'u_id' : self.u_id,
            'tokens' : self.token_list
        }

    def get_u_id_with_token(self, token):
        return u_id if token in self.token_list else -1
    

class Channel():

    def __init__(self, channel_id, name, message_id_list, u_id_list, owner_u_id_list, is_private):
        self.channel_id = channel_id
        self.name = name
        self.message_id_list = message_id_list
        self.u_id_list = u_id_list
        self.owner_u_id_list = owner_u_id_list
        self.is_private = is_private
    
    def get_channel_dict(self):
        return {
            'channel_id' : self.channel_id,
            'name' : self.name,
            'message_ids' : self.message_id_list,
            'u_ids' : self.u_id_list,
            'owner_u_ids' : self.owner_u_id_list,
            'is_private' : self.is_private
        }
    
    def add_new_member(self, u_id):
        self.u_id_list.append(u_id)
    
    def add_new_owner(self, u_id):
        self.owner_u_id_list.append(u_id)
    
    def remove_member(self, u_id):
        self.u_id_list.remove(u_id)
    
    def remove_owner(self, u_id):
        self.owner_u_id_list.remove(u_id)

class User():
    
    def __init__(self, u_id, email, name_first, name_last, handle_str):
        self.u_id = u_id
        self.email = email
        self.name_first = name_first
        self.nmae_last = name_last
        self.handle_str = handle_str
    
    def get_user_dict(self):
        return {
            'u_id' : self.u_id,
            'email' : self.email,
            'name_first' : self.name_first,
            'name_last' : self.nmae_last,
            'handle_str' : self.handle_str
        }

class Message():

    def __init__(self, message_id, u_id, message, time_created, react_list, is_pinned, is_private):
        self.message_id = message_id
        self.u_id = u_id
        self.message = message
        self.time_created = time_created
        self.react_list = react_list
        self.is_pinned = is_pinned
        self.is_private = is_private
    
    def get_message_dict(self):
        return {
            'message_id' : self.message_id,
            'u_id' : self.u_id,
            'message' : self.message,
            'time_created' : self.time_created,
            'reacts' : self.react_list,
            'is_pinned' : self.is_pinned 
        }
    
class Member():

    def __init__(self, u_id, name_first, name_last):
        self.u_id = u_id
        self.name_first = name_first
        self.name_last = name_last
    
    def get_member_dict(self):
        return {
            'u_id' : self.u_id,
            'name_first' : self.name_first,
            'name_last' : self.name_last
        }

class React():

    def __init__(self, react_id, u_id_list, is_this_user_reacted):
        self.react_id = react_id
        self.u_id_list = u_id_list
        self.is_this_user_reacted = is_this_user_reacted
    
    def get_react_dict(self):
        return {
            'react_id' : self.react_id,
            'u_ids' : self.u_id_list,
            'is_this_user_reacted' : self.is_this_user_reacted
        }
        
class Data():

    def __init__(self, user_list = [], message_list = [], channel_list = [], member_list = [], login_list = []):
        
        self.user_list = user_list
        self.message_list = message_list
        self.channel_list = channel_list
        self.member_list = member_list
        self.login_list = login_list
        
        self.next_u_id = -1
        self.next_channel_id = -1
        self.next_message_id = -1

    def add_channel(self, new_channel):
        self.channel_list.append(new_channel)
    
    def add_user(self, new_user):
        self.user_list.append(new_user)
    
    def add_message(self, new_message):
        self.message_list.append(new_message)
    
    def add_member(self, new_member):
        self.member_list(new_member)
    
    def add_login(self, new_login):
        self.login_list(new_login)

    def add_user_to_channel(self, u_id, channel_id, is_owner):
        channel = self.get_channel(channel_id)
        channel.add_new_member(u_id)
        if(is_owner):
            channel.add_new_owner(u_id)
    
    def remove_user_to_channel(self, u_id, channel_id, is_owner):
        channel = self.get_channel(channel_id)
        channel.remove_member(u_id)
        if(is_owner):
            channel.remove_owner(u_id) 
    
    def remove_channel(self, channel):
        self.channel_list.remove(channel)
    
    def remove_user(self, user):
        self.user_list.remove(user)
    
    def remove_message(self, message):
        self.message_list.remove(message)
    
    def remove_member(self, member):
        self.member_list.remove(member)
    
    def remove_login(self, login):
        self.login_list.remove(login)
    
    def get_channel(self, channel_id):
        for channel in self.channel_list:
            if(channel.get_channel_dict()['channel_id'] == channel_id):
                return channel
        return None
    
    def get_channel_dict(self, channel_id):
        return self.get_channel(channel_id).get_channel_dict() if self.get_channel(channel_id) else {}

    def get_user(self, u_id):
        for user in self.user_list:
            if(user.get_user_dict()['u_id'] == u_id):
                return user
        return None

    def get_user_dict(self, u_id):
        return self.get_user(u_id).get_user_dict() if self.get_user(u_id) else {}
  
    def get_message(self, message_id):
        for message in self.message_list:
            if(message.get_message_dict()['message_id'] == message_id):
                return message
        return None

    def get_message_dict(self, message_id):
        return self.get_message(message_id).get_message_dict() if self.get_message(message_id) else {}
    
    def get_memember(self, u_id):
        for member in self.member_list:
            if(member.get_member_dict()['u_id'] == u_id):
                return member
        return None
    
    def get_member_dict(self, u_id):
        return self.get_member(u_id).get_member_dict() if self.get_member(u_id) else {}

    def get_login(self, u_id):
        for login in self.login_list:
            if(login.get_login_dict()['u_id'] == u_id):
                return login
        return None
    
    def get_login_dict(self, u_id):
        return self.get_login(u_id).get_login_dict() if self.get_login(u_id) else {}
    
    def get_u_id_with_token(self, token):
        for login in self.login_list:
            if(login.get_u_id_with_token(token) > 0):
                return login.get_u_id_with_token()
        return -1
    
    def get_owner_u_ids_with_channel_id(self, ch_id):
        return self.get_channel_dict(ch_id)['owner_u_ids']
    
    def get_u_ids_with_channel_id(self, ch_id):
        return self.get_channel_dict(ch_id)['u_ids']
    
    def get_is_private_with_channel_id(self, ch_id):
        return self.get_is_private_with_channel_id(ch_id)['is_private']
    
    def get_all_u_ids(self):
        u_id_list = []
        for user in self.user_list:
            u_id_list.append(user.get_user_dict()['u_id'])
        return u_id_list
    
    def get_all_channel_ids(self):
        channel_id_list = []
        for channel in self.channel_list:
            channel_id_list.append(channel.get_channel_dict()['channel_id'])
        return channel_id_list

    def get_all_message_ids_in_a_channel(self, channel_id):
         return self.get_channel_dict(channel_id)['message_ids']   
    
    def gen_next_u_id(self):
        self.next_u_id += 1
        return self.next_u_id
    
    def gen_next_channel_id(self):
        self.next_channel_id += 1
        return self.next_channel_id
    
    def gen_next_message_id(self):
        self.next_message_id += 1
        return self.next_message_id
    
    def reset(self):
        self.user_list = []
        self.message_list = []
        self.channel_list = []
        self.member_list = []
        self.login_list = []
        
        self.next_u_id = -1
        self.next_channel_id = -1
        self.next_message_id = -1
        


# An example of data flow is as follow, you can write in your files "from Data import getData"

    # Create a global object data
data = Data()

def getData():
    global data
    return data

    # Create a new user
u_id = getData().gen_next_u_id()
user_example = User(u_id, '123@unsw.edu.au', 'Sunny', 'Qin', 'SunnyQin')
data.add_user(user_example)

    # get the user_dict with u_id
user_dict = getData().get_user_dict(u_id)
print(user_dict)
>>>>>>> dev2
