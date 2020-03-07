# Test Assumptions

## auth.py

## channel.py

### channel_invite()
- if user is not a member of channel then raise AccessError
- user immediately becomes channel member after invite
- returns empty list if user is member and has been reinvited
- if user or channel does not exist then raise InputError

### channel_details()
- returns tuple of channel name, list of owners, list of members
- only channel members may call details()
- if channel does not exist then raise InputError
- if user is not member of channel then raise AccessError

### channel_messages()
- return at most 50 messages from a given "start"
- index 0 message is most recent
- "end" 
- return -1 if no new messages

### channel_leave()


### channel_join()
- returns empty list on success


### channel_addowner()


### channel_removeowner()

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
- channel name can be empty, consist of only whitespace and be repeated
- channel_id is unique
    - unique channel id allows identification of channel for back-end
- incorrect channel names will throw InputError
    - channel name with char > 20 is over the limit and throws InputError

## echo.py

## error.py

## message.py

## other.py
- users_all doesn't return a list of users like the documentation. Rather, returns a dictionary with key value 'users' which contains a list of users like the skeleton function. 


## user.py
