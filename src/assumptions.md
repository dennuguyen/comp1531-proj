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
- user immmediately becomes channel member after being invited
- invite() returns empty list on success
- if inviter is not a member of channel then raise AccessError
- if user or channel does not exist then raise InputError
- token belongs to the inviter, user id belongs to the invitee

### channel_details()
- returns list of channel name, list of owners, list of members
- only channel members may call details()
- if channel id is not valid then raise InputError
- if user is not member of channel then raise AccessError

### channel_messages()
- returns a list of messages, start, end
- return at most 50 messages from a given "start"
- index 0 message is most recent
- "end" 
- return -1 if no new messages

### channel_leave()
- takes in token of user wanting to leave and the channel being left
- returns empty list on success
- if channel id is not valid then raise InputError
- if user id is not valid then raise AccessError

- **if user is last member of channel then user is owner and cannot leave the channel. Trying to do so will raise InputError**

### channel_join()
- returns empty list on success
- if user tries to join private channel then raise AccessError
- if channel id is not valid then raise InputError
- if member of channel tries to rejoin channel then join() succeeds

### channel_addowner()
- **return empty list on success**

### channel_removeowner()
- return empty list on success
- if user to be removed is not an owner then raise InputError
- if channel id is not valid then raise InputError
- when the user who is removing is not authorised then raise AccessError

## channels.py

### channels_list()
- returns a list of channels and their details
- shows channels user is part of
- invalid or no given token returns an empty list

### channels_listall()
- returns a list of channels and their details
- shows all channels regardless of membership
- invalid or no given token returns an empty list

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

### message_remove()
- if message no longer exists and is to be removed then throw InputError

## other.py

## user.py
