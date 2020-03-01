# Test Assumptions

## auth.py

## channel.py

### invite()


### details()


### messages()


### leave()


### channel_join()



### addowner()


### removeowner()

## channels.py

### list()
- returns a list of channels
- shows channels user is part of

### listall()
- returns a list of channels
- listall() will show all channels; except private channels excluding the user

### create()
- returns unique channel_id
- channel name cannot be empty
- channel name is unique
- channel name cannot consist of only whitespace
- incorrect channel names will throw InputError

## echo.py

## error.py

## message.py

## other.py

## user.py
