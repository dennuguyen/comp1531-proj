import json

data = {
'log_in' : [{'u_id' : 0, 'token' : 0}], # Stores logged in users
'users' : [{'u_id' : 0, 'email' : 0, 'name_first' : 0, 'name_last' : 0, 'handle_str' : 0, 'password' : 0}], # Stores registered users
'messages' : [{'message_id' : 0, 'u_id' : 0, 'message' : 0, 'time_created' : 0}], # Stores messages including details
'channels' : [{'channel_id' : 0,   
            'name' : 0, 
            'isprivate' : 0, 
            'owner_members' : [{'u_id' : 0, 'name_first' : 0, 'name_last' : 0}], 
            'all_members' : [{'u_id' : 0, 'name_first' : 0, 'name_last' : 0}], 
            'messages' : []}], # Stores channels including details
}
with open("data.json", "w+") as f:
    json.dump(data, f)