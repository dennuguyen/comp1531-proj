
import data

def channels_list(token):

    
    channel_id_list = 
    name_list = []

    for ch_id in channel_id_list:
            if u_id in ch_id.get_channel_dict()['uids']:
                channel_info = {'channel_id' : ch_id.get_channel_dict()['channel_id'],
                                'name' : ch_id.get_channel_dict()['name']}
                channels['channels'].append(channel_info)

    return {
        'channels': [
            {
                'channel_id': 1,
                'name': 'My Channel',
            }
        ],
    }


def channels_listall(token):
    """
    Returns a dictionary with key 'channels' and value that is a list of
    dictionaries with keys 'channel_id' and 'name'
    """

    channel_id_list = [channel.get_channel_id() for channel in data.get_data().get_channel_list()]
    channel_name_list = [channel.get_channel_name() for channel in data.get_data().get_channel_list()]

    # Hint: Use map() to split the list to assign the list element to key in dict

    return {
        'channels': [
            {
                'channel_id': 123,
                'name': 'channel_name_example',
            },
        ],
    }

# Check token is valid
# Check name is valid
def channels_create(token, name, is_public):
# Add channel to channel database and input details
# Generate channel id and input into channel database
    
    return {
        'channel_id': 1,
    }
