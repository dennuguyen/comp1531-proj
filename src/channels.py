'''
This module is concerned with the creation and documentation of channels.

channels_list(.) provides the user with details of all the channels he is in.

channels_listall(.) provides the user with details of all the channels.

channels_create(.) creates a new channel and puts the user who created it in it.
'''

import data
import authenticate as au

@au.authenticator(au.is_token_valid)
def channels_list(*, token):
    '''
    Provide a list of all channels (and their associated details)
    that the authorised user is part of
    '''
    # Get the User data class with token
    user = data.get_data().get_user_with_token(token)

    # Get a list of all the channels
    channels = data.get_data().get_channel_list()

    # Filter these channels to only include ones the user is in
    channels_user_in = filter(lambda channel: user.get_u_id() in channel.get_u_id_list(), channels)

    channels_dict = map(
        lambda channel: {
            'channel_id' : channel.get_channel_id(),
            'name' : channel.get_channel_name(),
            },
        channels_user_in,
    )

    # Return the channels_dict as a list, not map object
    return {'channels' : list(channels_dict)}

@au.authenticator(au.is_token_valid)
def channels_listall(*, token):
    """
    Provide a list of all channels (and their associated details)

    Returns a dictionary with key 'channels' and value that is a list of
    dictionaries with keys 'channel_id' and 'name'
    """
    # Get a list of all the channels
    channels = data.get_data().get_channel_list()

    # Transform this into a corresponding dictionary.
    channels_dict = map(
        lambda channel: {
            'channel_id' : channel.get_channel_id(),
            'name' : channel.get_channel_name(),
            },
        channels
    )

    # Return the channels_dict as a list, not map object
    return {'channels' : list(channels_dict)}


@au.authenticator(au.is_token_valid, au.channel_name_length)
def channels_create(*, token, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private channel
    '''
    # First get the user_id from the token
    user = data.get_data().get_user_with_token(token)
    u_id = user.get_u_id()

    # Generate a new channel id.
    new_channel_id = data.get_data().global_ch_id()

    # Create a new channel with the only member being the creator.
    u_id_list = [0, u_id]
    owner_u_id_list = [0, u_id]
    if u_id == 0:
        u_id_list = [u_id]
        owner_u_id_list = [u_id]
    new_channel = data.Channel(ch_id=new_channel_id,
                               ch_name=name,
                               msg_id_list=[],
                               u_id_list=u_id_list,
                               owner_u_id_list=owner_u_id_list,
                               is_public=is_public)

    

    # Append this to the dataset.
    data.get_data().add_channel(new_channel)

    # print("The channel length is: ")
    # print(len(data.get_data().get_channel_list()))

    return {
        'channel_id': new_channel_id,
    }
