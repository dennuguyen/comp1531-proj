import data

# @check_token_isvalid
# @check_channel_id_isvalid
# @check_token_isauthorised
# @check_u_id_isvalid
# @check_token_isnotmember

def channel_invite(token=str, channel_id=int, u_id=int):

# If all conditions are met add u_id to channel as member
    # Edit relevant databases
    datapy = data.Data()
    datapy.add_user_to_channel(u_id, channel_id, False)

    return {
    }

# @check_token_isvalid
# @check_channel_id_isvalid
# @check_token_isauthorised
def channel_details(token=str, channel_id=int):

# If all conditions are met 
    # Return {name, owner_members, all_members}
    datapy = data.Data()
    channel_dict = datapy.get_channel_dict(channel_id)
    channel_details = {'name' : channel_dict['name'], }


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

    datapy = data.Data()
    msg_id_list = datapy.get_all_message_ids_in_a_channel(channel_id)
    no_messages = len(msg_id_list)
    show = start + 50
    end_view = start + 50
    if no_messages < (start + 50):
        show = no_messages
        end_view = -1
        messages = []
    x = 1
    for i in msg_id_list and x <= show:
        messages.append(datapy.get_message_dict(i))
    return {'messages' : messages, 'start' : start, 'end' : end_view}


# @check_token_isvalid
# @check_channel_id_isvalid
# @check_token_isnotslackrking
# @check_token_ismember
def channel_leave(token=str, channel_id=int):

# If all conditions are met
    # Remove user from channel member list


    datapy = data.Data()
    u_id = datapy.get_u_id_with_token(token)
    u_id_list = datapy.get_owner_u_ids_with_channel_id(channel_id)
    if u_id in u_id_list:
        datapy.remove_user_to_channel(u_id, channel_id, True)
    datapy.remove_user_to_channel(u_id, channel_id, False)

    return {
    }

# @check_token_isvalid
# @check_channel_id_isvalid
# @check_channel_isnotprivate
def channel_join(token=str, channel_id=int):

# If all conditons are met
    # Add token to channel member list

    datapy = data.Data()
    u_id = datapy.get_u_id_with_token(token)
    datapy.add_user_to_channel(u_id, channel_id, False)

    return {
    }

# @check_token_isvalid
# @check_token_isowner
# @check_channel_id_isvalid
# @check_u_id_isnotowner
def channel_addowner(token=str, channel_id=int, u_id=int):

# If all conditons are met
    # Add u_id into channel owner list

    datapy = data.Data()
    u_id = datapy.get_u_id_with_token(token)
    datapy.remove_user_to_channel(u_id, channel_id, False)
    datapy.add_user_to_channel(u_id, channel_id, True)

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

    datapy = data.Data()
    datapy.remove_user_to_channel(u_id, channel_id, True)

    return {
    }


