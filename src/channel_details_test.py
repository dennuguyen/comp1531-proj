def test_channel_details():

    # create a user and channel
    u_id1, token1, ch_id = create_user_channel()
    u_id2, token2 = auth_register('max_is_cool@unsw.com', 'password', 'Max', 'Power')

    # invite John Doe to the channel
    channel_invite(token1, ch_id, u_id1)

    correct_detail = {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

    # call detail() as channel member
    assert channel_details(token1, ch_id) == correct_detail

    # call detail() as non-channel user
    assert channel_details(token2, ch_id) == correct_detail

    # invalid channel id
    with pytest.raises(InputError):
        channel_details(token1, ch_id + 1)

    # invalid user id
    with pytest.raises(InputError):
        channel_details(token1 + token2, ch_id)