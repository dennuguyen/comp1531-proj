# Test Assumptions

## auth.py

### auth_login()
- multiple logins are allowed and return the same u_id and token

### auth_logout()
- use of invalidated token returns False

### auth_register()
- when user registers, automatically login
- if user handle is already taken on register then concatenate a number and increment it for every taken user handle from 1
- the very first registered user is the slackr owner

## channel.py

### channel_invite()
- user immmediately becomes channel member after being invited
- returns empty list on success
- self-invitation if already a member does nothing as this can be a useful feature to find a particular channel

### channel_details()
- all_members key will include list of channel members including owners

### channel_messages()

### channel_leave()
- returns empty dictionary on success
- owners and members can leave the channel
- slackr owner attempting to leave the channel will raise InputError
- leaving a public channel has the same test environment as leaving a private channel

### channel_join()
- returns empty dictionary on success
- if member of channel tries to rejoin channel then raise InputError

### channel_addowner()
- return empty dictionary on success
- only members of the channel can be given owner permissions by an owner of that channel
- giving an owner owner permissions will raise InputError
- giving a stranger owner permissions will raise InputError

### channel_removeowner()
- return empty dictionary on success
- channel and slackr owner can remove other owner permissions
- slackr owner cannot be stripped of owner permissions

## channels.py

### channels_list()

### channels_listall()
- shows all channels regardless of membership

### channels_create()
- channel name can be repeated
- channel_id is unique
- channel name cannot be empty or consist of only whitespace
- user who creates the channel becomes the owner of the channel
- slackr owner is automatically invited to the channel as a channel owner

## echo.py

## message.py

### message_send()
- 

### message_remove()
- returns empty dictionary on success
- channel owner and slackr owner can remove messages

### message_edit()
- returns empty dictionary on success
- channel owner and slackr owner can edit messages
- editing messages updates the time and user id

## other.py
- users_all doesn't return a list of users like the documentation. Rather, returns a dictionary with key value 'users' which contains a list of users like the skeleton function. 

- search returns a dictionary with key value 'messages' which contains a list of messages datatype. 
- search does not return messages sent in public unless user has joined them.


## user.py
