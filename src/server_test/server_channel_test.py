"""
System testing module to assure general correctness of channel application
systems and http routes.

Black box testing is used as the functionality of the application's systems are
already covered with unit testing. Therefore it can be considered that these
tests are more concerned about the end-user's experience.

Requests Module Documentation:
https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
"""
import pytest
import data
import requests
import sys
sys.path.append("../")

BASE_URL = "http://127.0.0.1:8080"
HEADERS = {"Content-Type": "application/json"}


@pytest.fixture(autouse=True)
def reset_state():
    """
    This pytest fixture automatically runs for every test function call
    """
    r = requests.post(f"{BASE_URL}/workspace/reset")
    assert r.status_code == requests.codes.ok


def test_channel_membership(get_new_user_detail_1, get_new_user_detail_2):
    """
    Test channel creation, joining, invitation and leaving
    """
    # Get user 1 details
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    reg1 = {
        "email": email1,
        "password": password1,
        "name_first": name_first1,
        "name_last": name_last1,
    }

    # Get user 2 details
    email2, password2, name_first2, name_last2 = get_new_user_detail_2
    reg2 = {
        "email": email2,
        "password": password2,
        "name_first": name_first2,
        "name_last": name_last2,
    }

    # Register user 1
    r1 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg1)
    u_id1 = {"u_id": r1.json()["u_id"]}
    token1 = {"token": r1.json()["token"]}

    # Register user 2
    r2 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg2)
    u_id2 = {"u_id": r2.json()["u_id"]}
    token2 = {"token": r2.json()["token"]}

    # User 1 creates two channels
    ch1 = {**token1, **{"name": "Cowabunga", "is_public": True}}
    r3 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json=ch1)
    assert r3.status_code == requests.codes.ok

    r4 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json=ch1)
    assert r4.status_code == requests.codes.ok

    # Get the channel ids
    ch_id1 = {"channel_id": r3.json()["channel_id"]}
    ch_id2 = {"channel_id": r4.json()["channel_id"]}
    assert ch_id1 != ch_id2

    # User 2 is invited to first channel by user 1
    inv1 = {**token1, **ch_id1, **u_id2}
    r5 = requests.post(f"{BASE_URL}/channel/invite",
                       headers=HEADERS,
                       json=inv1)
    assert r5.status_code == requests.codes.ok

    # User 2 joins the second channel
    inv2 = {**token2, **ch_id2}
    r6 = requests.post(f"{BASE_URL}/channel/join", headers=HEADERS, json=inv2)
    assert r6.status_code == requests.codes.ok

    # User 2 leaves first channel
    leave1 = {**token2, **ch_id1}
    r7 = requests.post(f"{BASE_URL}/channel/leave",
                       headers=HEADERS,
                       json=leave1)
    assert r7.status_code == requests.codes.ok  # TODO: 500

    # User 2 leaves second channel
    leave2 = {**token2, **ch_id2}
    r8 = requests.post(f"{BASE_URL}/channel/leave",
                       headers=HEADERS,
                       json=leave2)
    assert r8.status_code == requests.codes.ok

    # User 1 check channel details
    cdet1 = {**token1, **ch_id1}
    r9 = requests.get(f"{BASE_URL}/channel/details", cdet1)
    assert len(r9.json()['all_members']) == 1
    assert r9.status_code == requests.codes.ok


def test_channel_membership_exception_handling(get_new_user_detail_1,
                                               get_new_user_detail_2,
                                               get_new_user_detail_3):
    """
    Test channel creation, joining, invitation and leaving
    """
    # Get user 1 details
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    reg1 = {
        "email": email1,
        "password": password1,
        "name_first": name_first1,
        "name_last": name_last1,
    }

    # Get user 2 details
    email2, password2, name_first2, name_last2 = get_new_user_detail_2
    reg2 = {
        "email": email2,
        "password": password2,
        "name_first": name_first2,
        "name_last": name_last2,
    }

    # Register user 1
    r1 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg1)
    u_id1 = {"u_id": r1.json()["u_id"]}
    token1 = {"token": r1.json()["token"]}

    # Register user 2
    r2 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg2)
    u_id2 = {"u_id": r2.json()["u_id"]}
    token2 = {"token": r2.json()["token"]}

    # User 1 creates two channels
    ch1 = {**token1, **{"name": "Cowabunga", "is_public": False}}
    r3 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json=ch1)
    assert r3.status_code == requests.codes.ok

    # Get the channel ids
    ch_id1 = {"channel_id": r3.json()["channel_id"]}

    # User 2 invited to channel
    inv1 = {**token1, **ch_id1, **u_id2}
    r4 = requests.post(f"{BASE_URL}/channel/invite",
                       headers=HEADERS,
                       json=inv1)
    assert r4.status_code == requests.codes.ok

    # User 2 leaves channel
    leave1 = {**token2, **ch_id1}
    r5 = requests.post(f"{BASE_URL}/channel/leave",
                       headers=HEADERS,
                       json=leave1)
    assert r5.status_code == requests.codes.ok

    # User 2 joins the channel
    join2 = {**token2, **ch_id1}
    with pytest.raises(requests.RequestException):
        requests.post(f"{BASE_URL}/channel/join", headers=HEADERS,
                      json=join2).raise_for_status()

    # User 1 check channel details
    cdet1 = {**token1, **ch_id1}
    r6 = requests.get(f"{BASE_URL}/channel/details", cdet1)
    assert len(r6.json()['all_members']) == 1
    assert r6.status_code == requests.codes.ok


def test_channel_ownership(get_new_user_detail_1, get_new_user_detail_2,
                           get_new_user_detail_3):
    """
    Test channel creation, inviting, addowner and remove owner
    """
    # Get user 1 details
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    reg1 = {
        "email": email1,
        "password": password1,
        "name_first": name_first1,
        "name_last": name_last1,
    }

    # Get user 2 details
    email2, password2, name_first2, name_last2 = get_new_user_detail_2
    reg2 = {
        "email": email2,
        "password": password2,
        "name_first": name_first2,
        "name_last": name_last2,
    }

    # Get user 3 details
    email3, password3, name_first3, name_last3 = get_new_user_detail_3
    reg3 = {
        "email": email3,
        "password": password3,
        "name_first": name_first3,
        "name_last": name_last3,
    }

    # Register user 1
    r1 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg1)
    token1 = {"token": r1.json()["token"]}

    # Register user 2
    r2 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg2)
    u_id2 = {"u_id": r2.json()["u_id"]}
    token2 = {"token": r2.json()["token"]}

    # Register user 3
    r3 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg3)
    u_id3 = {"u_id": r3.json()["u_id"]}
    token3 = {"token": r3.json()["token"]}

    # User 1 creates a channels
    ch1 = {**token1, **{"name": "Cowabunga", "is_public": True}}
    r4 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json=ch1)
    assert r4.status_code == requests.codes.ok

    # Get the channel ids
    ch_id1 = {"channel_id": r4.json()["channel_id"]}

    # User 2 is invited to channel by user 1
    inv1 = {**token1, **ch_id1, **u_id2}
    r5 = requests.post(f"{BASE_URL}/channel/invite",
                       headers=HEADERS,
                       json=inv1)
    assert r5.status_code == requests.codes.ok

    # User 3 is invited to channel by user 1
    inv2 = {**token1, **ch_id1, **u_id3}
    r6 = requests.post(f"{BASE_URL}/channel/invite",
                       headers=HEADERS,
                       json=inv2)
    assert r6.status_code == requests.codes.ok

    # User 2 is added as owner to channel by user 1
    add1 = {**token1, **ch_id1, **u_id2}
    r7 = requests.post(f"{BASE_URL}/channel/addowner",
                       headers=HEADERS,
                       json=add1)
    assert r6.status_code == requests.codes.ok

    # User 1 check channel details
    cdet1 = {**token1, **ch_id1}
    r7 = requests.get(f"{BASE_URL}/channel/details", cdet1)
    assert len(r7.json()['owner_members']) == 2

    # User 3 remove user2 as owner
    rem1 = {**token3, **ch_id1, **u_id2}
    r8 = requests.post(f"{BASE_URL}/channel/removeowner",
                       headers=HEADERS,
                       json=rem1)
    assert r8.status_code != requests.codes.ok

    # User 3 is added as owner to channel by user 1
    add2 = {**token1, **ch_id1, **u_id3}
    r9 = requests.post(f"{BASE_URL}/channel/addowner",
                       headers=HEADERS,
                       json=add2)
    assert r9.status_code == requests.codes.ok

    # User 1 check channel details
    cdet1 = {**token1, **ch_id1}
    r9 = requests.get(f"{BASE_URL}/channel/details", cdet1)
    assert len(r9.json()['owner_members']) == 3

    # User 3 remove user2 as owner
    rem2 = {**token3, **ch_id1, **u_id2}
    r10 = requests.post(f"{BASE_URL}/channel/removeowner",
                        headers=HEADERS,
                        json=rem2)
    assert r10.status_code == requests.codes.ok

    # User 1 check channel details
    cdet1 = {**token1, **ch_id1}
    r10 = requests.get(f"{BASE_URL}/channel/details", cdet1)
    assert len(r10.json()['owner_members']) == 2


def test_channel_messages(get_new_user_detail_1, get_new_user_detail_2,
                          get_new_user_detail_3):
    """
    Test channel creation, inviting, addowner and remove owner
    """
    # Get user 1 details
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    reg1 = {
        "email": email1,
        "password": password1,
        "name_first": name_first1,
        "name_last": name_last1,
    }

    # Get user 2 details
    email2, password2, name_first2, name_last2 = get_new_user_detail_2
    reg2 = {
        "email": email2,
        "password": password2,
        "name_first": name_first2,
        "name_last": name_last2,
    }

    # Get user 3 details
    email3, password3, name_first3, name_last3 = get_new_user_detail_3
    reg3 = {
        "email": email3,
        "password": password3,
        "name_first": name_first3,
        "name_last": name_last3,
    }

    # Register user 1
    r1 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg1)
    u_id1 = {"u_id": r1.json()["u_id"]}
    token1 = {"token": r1.json()["token"]}

    # Register user 2
    r2 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg2)
    u_id2 = {"u_id": r2.json()["u_id"]}
    token2 = {"token": r2.json()["token"]}

    # Register user 3
    r3 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg3)
    u_id3 = {"u_id": r3.json()["u_id"]}
    token3 = {"token": r3.json()["token"]}

    # User 1 creates a channels
    ch1 = {**token1, **{"name": "Cowabunga", "is_public": True}}
    r4 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json=ch1)
    assert r4.status_code == requests.codes.ok

    # Get the channel ids
    ch_id1 = {"channel_id": r4.json()["channel_id"]}

    # User 2 is invited to channel by user 1
    inv1 = {**token1, **ch_id1, **u_id2}
    r5 = requests.post(f"{BASE_URL}/channel/invite",
                       headers=HEADERS,
                       json=inv1)
    assert r5.status_code == requests.codes.ok

    # Send messages
    for i in range(75):
        msg = {'message': 'Test message'}
        msg1 = {**token1, **ch_id1, **msg}
        r7 = requests.post(f"{BASE_URL}/message/send",
                           headers=HEADERS,
                           json=msg1)
        assert r7.json()['message_id'] == i
        assert r7.status_code == requests.codes.ok

    # Check messages start less than number of messages
    cmsg1 = {**token1, **ch_id1, **{'start': '25'}}
    r8 = requests.get(f"{BASE_URL}/channel/messages", cmsg1)
    assert len(r8.json()['messages']) == 50
    assert r8.status_code == requests.codes.ok

    # Check messages start greater than number of messages
    cmsg2 = {**token1, **ch_id1, **{'start': '80'}}
    with pytest.raises(requests.RequestException):
        requests.get(f"{BASE_URL}/channel/messages", cmsg2).raise_for_status()

    # User 2 Check messages in channel
    cmsg3 = {**token2, **ch_id1, **{'start': '25'}}
    r9 = requests.get(f"{BASE_URL}/channel/messages", cmsg3)

    assert len(r8.json()['messages']) == 50
    assert r9.status_code == requests.codes.ok

    # Check messages start greater than number of messages
    cmsg4 = {**token3, **ch_id1, **{'start': '25'}}
    with pytest.raises(requests.RequestException):
        requests.get(f"{BASE_URL}/channel/messages", cmsg4).raise_for_status()
