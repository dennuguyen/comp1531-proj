'''
Notes:
1. Think what possible case you want to test in real life, and simulate that in the test
2. Normally use import <filename> and then use filename.function()
3. Assume functions are working 
4. Make sure test are usable for iteration 2 & 3
5. Don't worry about clean up in iteratin 1
6. Go for minimum number of tests maximum coverage

'''

import auth

def test_login():
    ################## SET UP STATE ######################


    # dummy data
    email, password = "123@124.com","qwetyu"
    
    #  valid u_id and token *we don't care about token*
    u_id, token = auth.auth_register(email, password)

    # log user we just created out
    auth_logout(token)
##############################################################


################## ACTUAL TEST ###############################
    test_u_id, _ = auth.auth_login(email, password)


    assert(u_id == test_u_id)

################## CLEAN UP (if necessary) ###################


def test_login_already_logged_in():


