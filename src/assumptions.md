# Test Assumptions

## auth.py

## channel.py

### invite()
- if user is not a member of channel then raise AccessError
- user immediately becomes channel member after invite
- returns empty list if user is member and has been reinvited
- if user or channel does not exist then raise InputError

### details()
- 

### messages()


### leave()


### channel_join()
- returns empty list on success


### addowner()


### removeowner()

## channels.py

### list()
- returns a list of channels
- shows channels user is part of
- invalid or no given token returns an empty list

### listall()
- returns a list of channels
- shows all channels regardless of membership
- invalid or no given token returns an empty list

### create()
- channel name cannot be empty or consist of only whitespace:
    - channel names should describe the purpose of the channel
    - empty channel names do not describe purpose
- channel name and channel_id are unique
    - repeated channel name will cause confusion for user and purpose of channel
    - unique channel id allows identification of channel for back-end
- incorrect channel names will throw InputError
    - channel name with char > 20 is over the limit and throws InputError

## echo.py

## error.py

## message.py

## other.py

## user.py
