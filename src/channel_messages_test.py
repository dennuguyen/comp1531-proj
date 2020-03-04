def test_channel_messages():

    # create a user and channel
    u_id, token, ch_id = create_user_channel()
    channel_invite(token, ch_id, u_id) # add user to channel

    # add some messages to the channel

    # if message length <= 50


    # if messages length > 50

    # no new messages
    assert channel_details(token, ch_id) == -1

    # start is greater than total number of msgs
    with pytest.raises

    # invalid channel id
    with pytest.raises(InputError):
        channel_details(token1, ch_id + 1)

    # invalid user id
    with pytest.raises(AccessError):
        channel_details(token1 + token2, ch_id)
