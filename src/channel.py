'''channel.py'''
import data
import authenticate as au



# Invite a user into channel as member
@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_not_member, au.check_u_id_existence)
def channel_invite(token=str, channel_id=int, u_id=int):

    # Add u_id into channel member list

    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    channel.add_new_member(u_id)
    return {
    }


# Return details of channel that requester is member of
@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_user_in_channel)
def channel_details(token=str, channel_id=int):

    # Retrieve information from database

    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    channel_det = {}
    channel_det['name'] = channel.get_channel_dict()['name']
    owner_list = channel.get_u_id_list()
    for u_id in owner_list:
        member_info = datapy.get_user_with_u_id(u_id)
        channel_det['owner_members'].append(member_info)
    
    all_list = channel.get_owner_u_id_list()
    for u_id in all_list:
        owner_info = datapy.get_user_with_u_id(u_id)
        channel_det['all_members'].append(owner_info)

    # Return {name, owner_members, all_members}
    return channel_det


# Return messages in a channel that requester is member of
@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_user_in_channel, au.start_has_more_messages)
def channel_messages(token=str, channel_id=int, start=int):

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

    channel_msg = {}
    msg_info = {}
    msg_list = datapy.get_message_list()

    i = start
    while  i < show:
        for msg in msg_list:
            msg_dict = msg.get_message_dict()
            if msg_dict['message_id'] == msg_id_list[i]:
                msg_info['message_id'] == msg_dict['message_id']
                msg_info['u_id'] == msg_dict['u_id']
                msg_info['message'] == msg_dict['message']
                msg_info['time_created'] == msg_dict['time_created']
                channel_msg['messages'].append(msg_info)
        i += 1
    channel_msg['start'] = start
    channel_msg['end'] = end_view

    # Return a dictionary of message info
    return channel_msg


# Leave a channel
@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_user_in_channel, au_is_not_slackr_owner)
def channel_leave(token=str, channel_id=int):


    # Remove user from channel member list

    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    login = datapy.get_login_with_token(token)
    u_id = login.u_id

    if u_id in channel.get_owner_u_id_list():
        channel.remove_owner(u_id)
    channel.remove_member(u_id)

    return {
    }


# Join a public channel as member
@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_private_not_admin)
def channel_join(token=str, channel_id=int):

    # Add u_id to channel member list

    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    login = datapy.get_login_with_token(token)
    u_id = login.u_id
    channel.add_new_member(u_id)

    return {
    }


# Add a member as an owner of channel
@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_admin_or_owner, au.not_ch_owner_or_owner, au.is_user_in_channel)
def channel_addowner(token=str, channel_id=int, u_id=int):

    # Add u_id into channel owner list

    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    login = datapy.get_login_with_token(token)
    u_id = login.u_id
    channel.add_new_owner(u_id)

    return {
    }


# Remove owner from owner list
@au.authenticator(au.is_token_valid, au.valid_channel_id, au.is_admin_or_owner, au.is_user_in_channel)
def channel_removeowner(token=str, channel_id=int, u_id=int):

    # Remove u_id from channel owner list

    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    login = datapy.get_login_with_token(token)
    u_id = login.u_id
    channel.remove_owner(u_id)

    return {
    }



