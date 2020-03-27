'''channel.py'''
import data
import authenticate as au



# Invite a user into channel as member
@au.authenticator(au.is_token_valid,
                  au.is_token_in_channel,
                  au.check_u_id_existence,
                  au.is_user_not_in_channel)
def channel_invite(*, token, channel_id, u_id):
    '''
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately
    '''
    # Get corresponding Channel class with channel_id
    channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

    # Add user to channel with corresponding id.
    channel_with_id.add_new_member(u_id)
    return {
    }


# Return details of channel that requester is member of
@au.authenticator(au.is_token_valid,
                  au.valid_channel_id,
                  au.is_not_member)
def channel_details(*, token, channel_id):
    '''
    Given a Channel with ID channel_id that the authorised user is part of.
    Provide basic details about the channel.
    '''

    # Get corresponding channel with channel_id
    channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

    # Get channel name
    name = channel_with_id.get_channel_name()

    # Get a list of all user member ids
    all_member_ids = channel_with_id.get_u_id_list()

    # Transform the list of user ids into User classes
    all_users = map(lambda id: data.get_data().get_user_with_u_id(id), all_member_ids)
    
    # Transform the mapping of users into a mapping of member dicts
    all_members = map(lambda user: user.get_member_details_dict(), all_users)

    # Get a list of all owner member ids
    owner_ids = channel_with_id.get_owner_u_id_list()

    # Transform the list of user ids into User classes
    owners = map(lambda id: data.get_data().get_user_with_u_id(id), owner_ids)
    
    # Transform the mapping of users into a mapping of member dicts
    owner_members = map(lambda user: user.get_member_details_dict(), owners)

    # Return {name, owner_members, all_members}
    return {
        'name' : name,
        'owner_members' : list(owner_members),
        'all_members' : list(all_members)
    }


# Return messages in a channel that requester is member of
@au.authenticator(au.is_token_valid,
                  au.valid_channel_id,
                  au.start_has_more_messages,
                  au.is_not_member)
def channel_messages(*, token, channel_id, start):
    '''
    Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50" inclusive.
    Message with index 0 is the most recent message in the channel.
    This function returns a new index "end" which is the value of "start + 50",
    or, if this function has returned the least recent messages in the channel,
    returns -1 in "end" to indicate there are no more messages to load after this return.
    '''

    # Retrieve messages from database

    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    msg_id_list = channel.get_msg_id_list()

    no_messages = len(msg_id_list)
    show = start + 50
    end_view = start + 50
    if no_messages < (start + 50):
        show = no_messages
        end_view = -1

    channel_msg = {'messages':[]}
    msg_info = {}
    msg_list = datapy.get_message_list()

    i = start
    while  i < show:
        for msg in msg_list:
            msg_dict = msg.get_message_dict()
            if msg_dict['message_id'] == msg_id_list[i]:
                msg_info['message_id'] = msg_dict['message_id']
                msg_info['u_id'] = msg_dict['u_id']
                msg_info['message'] = msg_dict['message']
                msg_info['time_created'] = msg_dict['time_created']
                channel_msg['messages'].append(msg_info)
        i += 1
    channel_msg['start'] = start
    channel_msg['end'] = end_view

    # Return a dictionary of message info
    return channel_msg


# Leave a channel
@au.authenticator(au.is_token_valid,
                  au.valid_channel_id,
                  au.is_not_member,
                  au.is_not_slackr_owner)
def channel_leave(*, token, channel_id):
    '''
    Given a channel ID, the user removed as a member of this channel.
    '''

    # Get Channel class with the channel_id
    channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

    # Get the corresponding User id with the token
    user_with_token = data.get_data().get_user_with_token(token)
    u_id = user_with_token.get_u_id()

    if u_id in channel_with_id.get_owner_u_id_list():
        channel_with_id.remove_owner(u_id)
    channel_with_id.remove_member(u_id)

    return {

    }


# Join a public channel as member
@au.authenticator(au.is_token_valid,
                  au.valid_channel_id,
                  au.is_private_not_admin,
                  au.is_token_not_in_channel)
def channel_join(*, token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join, adds them to that channel
    '''

    # Get u_id using the token
    user = data.get_data().get_user_with_token(token)
    u_id = user.get_u_id()

    # Get the corresponding channel with channel_id
    channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

    # Add the u_id to the channel
    channel_with_id.add_new_member(u_id)

    return {
    }


# Add a member as an owner of channel
@au.authenticator(au.is_token_valid,
                  au.valid_channel_id,
                  au.already_owner,
                  au.is_owner_or_slackr_owner,
                  au.is_user_in_channel,
                  au.check_u_id_existence)
def channel_addowner(*, token, channel_id, u_id):
    '''
    Make user with user id u_id an owner of this channel.
    '''

    # Get corresponding channel with channel id
    channel_with_id = data.get_data().get_channel_with_ch_id(channel_id)

    # Add user with u_id as an owner.
    channel_with_id.add_new_owner(u_id)

    return {
    }


# Remove owner from owner list
@au.authenticator(au.is_token_valid,
                  au.valid_channel_id,
                  au.not_owner,
                  au.is_owner_or_slackr_owner,
                  au.is_not_owner_of_slackr,
                  au.is_not_self,
                  au.check_u_id_existence)
def channel_removeowner(*, token, channel_id, u_id):
    '''
    Remove user with user id u_id an owner of this channel.
    '''

    # Get channel with channel_id
    channel = data.get_data().get_channel_with_ch_id(channel_id)

    # Remove the owner with u_id.
    channel.remove_owner(u_id)

    return {
    }
