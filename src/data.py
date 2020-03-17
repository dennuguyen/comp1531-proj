import json

data = {
'users' : [{'u_id' : 0, 'email' : 0, 'name_first' : 0, 'name_last' : 0, 'handle_str' : 0}], # list of different user
'messages' : [{'message_id' : 0, 'u_id' : 0, 'message' : 0, 'time_created' : 0}], # list of different message
'channels' : [{'channel_id' : 0, 'name' : 0}], # list of different channel
'channels_info' : [{'name' : 0, 'isprivate' : 0, 'owner_members' : [{'u_id' : 0, 'name_first' : 0, 'name_last' : 0}], 'name_last' : [{'u_id' : 0, 'name_first' : 0, 'name_last' : 0}]}], # list of different channels info
}
with open("data.json", "w+") as f:
    json.dump(data, f)