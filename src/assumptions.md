# Test Assumptions

## auth.py

### auth_login()
- multiple logins are allowed and return the same u_id but different token

### auth_logout()
- valid token allows successful logout
- logout without valid token returns False

### auth_register()
- when user registers, automatically login
- if user handle is alraedy taken on register then suffix a number

## channel.py

### channel_invite()
- user immmediately becomes channel member after being invited
- returns empty list on success
- self-invitation does nothing

### channel_details()
- all_members key will include list of channel members including owners

### channel_messages()

### channel_leave()
- returns empty dictionary on success

- if user is last member of channel then user is owner and cannot leave the channel. Trying to do so will raise InputError

### channel_join()
- returns empty dictionary on success
- if member of channel tries to rejoin channel then do nothing

### channel_addowner()
- return empty dictionary on success
- only members of the channel can be given owner permissions by an owner
- giving an owner owner permissions will raise InputError

### channel_removeowner()
- return empty dictionary on success
- there must always be at least 1 owner in any channel

## channels.py

### channels_list()

### channels_listall()
- shows all channels regardless of membership

### channels_create()
- channel name can be repeated o users who want to make channels with the same name can be happy
- channel_id is unique
- channel name cannot be empty or consist of only whitespace
- user who creates the channel becomes the owner of the channel because otherwise there will be no user with permissions to add other users to the channel or edit the channel

## echo.py

## message.py

### message_send()
- 

### message_remove()
- returns empty dictionary on success

## other.py
- users_all doesn't return a list of users like the documentation. Rather, returns a dictionary with key value 'users' which contains a list of users like the skeleton function. 

- search returns a dictionary with key value 'messages' which contains a list of messages datatype. 
- search does not return messages sent in public unless user has joined them.


## user.py

### user_profile()
- 
