'''channel.py'''
import data
import authenticate



# @check_token_isvalid
# @check_channel_id_isvalid
# @check_token_isauthorised
# @check_u_id_isvalid
# @check_u_id_isnotowner
def channel_invite(token=str, channel_id=int, u_id=int):

# If all conditions are met add u_id to channel as member
    # Edit relevant databases
    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    channel.add_new_member(u_id)
    return {
    }

# @check_token_isvalid
# @check_channel_id_isvalid
# @check_token_isauthorised
def channel_details(token=str, channel_id=int):

# If all conditions are met 
    # Return {name, owner_members, all_members}
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

    return channel_det



# @check_token_isvalid
# @check_channel_id_isvalid
# @check_token_isauthorised
# @check_start_issmaller
def channel_messages(token=str, channel_id=int, start=int):
    
# If all conditions are met
    # If end is less than total messages
        # Return {messages, start, end}
    # Else if end is greater than total messages
        # Return {messages, start, -1}

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

    return channel_msg


# @check_token_isvalid
# @check_channel_id_isvalid
# @check_token_isnotslackrking
# @check_token_ismember
def channel_leave(token=str, channel_id=int):

# If all conditions are met
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

# @check_token_isvalid
# @check_channel_id_isvalid
# @check_channel_isnotprivate
def channel_join(token=str, channel_id=int):

# If all conditons are met
    # Add token to channel member list

    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    login = datapy.get_login_with_token(token)
    u_id = login.u_id
    channel.add_new_member(u_id)

    return {
    }

# @check_token_isvalid
# @check_token_isowner
# @check_channel_id_isvalid
# @check_u_id_isnotowner
# @check_u_id_is_member
def channel_addowner(token=str, channel_id=int, u_id=int):

# If all conditons are met
    # Add u_id into channel owner list

    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    login = datapy.get_login_with_token(token)
    u_id = login.u_id
    channel.add_new_owner(u_id)

    return {
    }

# @check_token_isvalid
# @check_token_isowner
# @check_u_id_isvalid
# @check_channel_id_isvalid
# @check_u_id_isowner
def channel_removeowner(token=str, channel_id=int, u_id=int):

# If all conditons are met
    # Remove u_id from channel owner list

    datapy = data.get_data()
    channel = datapy.get_channel_with_ch_id(channel_id)
    login = datapy.get_login_with_token(token)
    u_id = login.u_id
    channel.remove_owner(u_id)

    return {
    }



