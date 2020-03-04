# Test Assumptions

## auth.py

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

- **user who creates the channel becomes the owner of the channel**

## echo.py

## error.py

## message.py

## other.py

## user.py
