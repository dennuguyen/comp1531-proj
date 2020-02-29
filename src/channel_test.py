import channel

# invite() should return an empty list on success?
def invite_test():

    assert invite('123', 12, 32) == {}
    # assert invite('123', 'a', 'b') == 

# details() returns channel details of channel_id upon valid token
# def details_test():
#     assert details()