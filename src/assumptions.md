# Test Assumptions

## auth.py

### auth_login()
- valid token is generated when receiving a registered user's email and password
- invalid email, password or unregistered email raises InputError
- user id and token is returned from login
- **multiple logins are allowed and return the same u_id but different token**

### auth_logout()
- valid token allows successful logout
- **logout without valid token returns False**

### auth_register()
- takes email, password, first name and last name
- returns list of token and user id on success
- invalid email raises InputError
- email already registered raises InputError
- password less than 6 char
- name_first between 1 and 50 char
- name_last between 1 and 50 char
- **when user registers, automatically login**

## channel.py

### channel_invite()
- **user immmediately becomes channel member after being invited**
- **returns empty list on success**
- **self-invitation does nothing**

### channel_details()
- returns list of channel name, list of owners, list of members
- only channel members may call details()
- if channel id is not valid then raise InputError
- if user is not member of channel then raise AccessError
- **all_members key will include list of channel members including owners**

### channel_messages()
- returns a list of messages, start, end
- return at most 50 messages from a given "start"
- index 0 message is most recent
- "end" 
- return -1 if no new messages

### channel_leave()
- takes in token of user wanting to leave and the channel being left
- **returns empty dictionary on success**
- if channel id is not valid then raise InputError
- if user id is not valid then raise AccessError

- **if user is last member of channel then user is owner and cannot leave the channel. Trying to do so will raise InputError**

### channel_join()
- **returns empty dictionary on success**
- if user tries to join private channel then raise AccessError
- if channel id is not valid then raise InputError
- if member of channel tries to rejoin channel then join() succeeds

### channel_addowner()
- **return empty dictionary on success**
- **only members of the channel can be given owner permissions by an owner**
- **giving an owner owner permissions will raise InputError**

### channel_removeowner()
- **return empty dictionary on success**
- if user to be removed is not an owner then raise InputError
- if channel id is not valid then raise InputError
- when the user who is removing is not authorised then raise AccessError

## channels.py

### channels_list()
- returns a list of channels and their details
- shows channels user is part of

### channels_listall()
- returns a list of channels and their details
- shows all channels regardless of membership

### channels_create()
- **channel name can be repeated**
    - so users who want to make channels with the same name can be happy
- **channel_id is unique**
    - unique channel id allows identification of channel for back-end
- **channel name cannot be empty or consist of only whitespace**
    - because names cannot be empty
- **user who creates the channel becomes the owner of the channel**
    - because otherwise there will be no user with permissions to add other users to the channel or edit the channel

## echo.py

## message.py

### message_send()
- 

### message_remove()
- if message no longer exists and is to be removed then raise InputError
- only owner and user who sent message can remove message else raise AccessError
- **returns empty dictionary on success**

## other.py
- users_all doesn't return a list of users like the documentation. Rather, returns a dictionary with key value 'users' which contains a list of users like the skeleton function. 

- search returns a dictionary with key value 'messages' which contains a list of messages datatype. 
- search does not return messages sent in public unless user has joined them.


## user.py
