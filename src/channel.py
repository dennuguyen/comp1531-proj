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
    return datapy.get_channel_dict(channel_id)

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

    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

# @check_token_isvalid
# @check_channel_id_isvalid
# @check_token_isnotslackrking
# @check_token_ismember
def channel_leave(token=str, channel_id=int):

# If all conditions are met
    # Remove user from channel member list

    return {
    }

# @check_token_isvalid
# @check_channel_id_isvalid
# @check_channel_isnotprivate
def channel_join(token=str, channel_id=int):

# If all conditons are met
    # Add token to channel member list

    return {
    }

# @check_token_isvalid
# @check_token_isowner
# @check_channel_id_isvalid
# @check_u_id_isnotowner
def channel_addowner(token=str, channel_id=int, u_id=int):

# If all conditons are met
    # Add u_id into channel owner list

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

    return {
    }


