"""
System testing module to assure general correctness of message application
systems and http routes.

Black box testing is used as the functionality of the application's systems are
already covered with unit testing. Therefore it can be considered that these
tests are more concerned about the end-user's experience.

Requests Module Documentation:
https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
"""
import pytest
import requests
import time
import sys
sys.path.append("../")
import server
import data

BASE_URL = "http://127.0.0.1:8080"
HEADERS = {"Content-Type": "application/json"}


@pytest.fixture(autouse=True)
def reset_state():
    """
    This pytest fixture automatically runs for every test function call
    """
    r = requests.post(f"{BASE_URL}/workspace/reset")
    assert r.status_code == requests.codes.ok


def test_message_send_edit(get_new_user_detail_1, get_new_user_detail_2):
    """
    Test message sending, editing and removing
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
    token1 = {"token": r1.json()["token"]}

    # Register user 2
    r2 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg2)
    token2 = {"token": r2.json()["token"]}

    # User 1 creates a channel
    ch1 = {**token1, **{"name": "Cowabunga", "is_public": True}}
    r3 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json=ch1)
    ch_id1 = {"channel_id": r3.json()["channel_id"]}

    # User 2 joins the channel
    requests.post(f"{BASE_URL}/channel/join",
                  headers=HEADERS,
                  json={
                      **token2,
                      **ch_id1
                  })

    # User 1 sends a message
    msg1 = {
        **token1,
        **ch_id1,
        **{
            "message": "This channel is cool",
            "time_sent": time.time(),
        },
    }
    r4 = requests.post(f"{BASE_URL}/message/send", headers=HEADERS, json=msg1)
    assert r4.status_code == requests.codes.ok

    # User 2 sends a message
    msg2 = {
        **token2,
        **ch_id1,
        **{
            "message": "No it isn't",
            "time_sent": time.time(),
        },
    }
    r5 = requests.post(f"{BASE_URL}/message/send", headers=HEADERS, json=msg2)
    assert r5.status_code == requests.codes.ok

    # Get msg2's id
    msg_id2 = {"message_id": r5.json()["message_id"]}

    # User 1 edits user 2's message
    edit = {
        **token1,
        **msg_id2,
        **{
            "message": "Yes it is",
        },
    }
    r6 = requests.put(f"{BASE_URL}/message/edit", headers=HEADERS, json=edit)
    assert r6.status_code == requests.codes.ok

    # User 2 removes their own message
    rmv = {**token2, **msg_id2}
    r7 = requests.delete(f"{BASE_URL}/message/remove",
                         headers=HEADERS,
                         json=rmv)
    assert r7.status_code == requests.codes.ok


def test_message_send_edit_exception_handling(get_new_user_detail_1,
                                              get_new_user_detail_2):
    """
    Test message sending, editing and removing exception handling
    """
    # Get user 1 and 2 details
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    email2, password2, name_first2, name_last2 = get_new_user_detail_2

    # Register users 1 and 2
    r1 = requests.post(f"{BASE_URL}/auth/register",
                       headers=HEADERS,
                       json={
                           "email": email1,
                           "password": password1,
                           "name_first": name_first1,
                           "name_last": name_last1,
                       })
    r2 = requests.post(f"{BASE_URL}/auth/register",
                       headers=HEADERS,
                       json={
                           "email": email2,
                           "password": password2,
                           "name_first": name_first2,
                           "name_last": name_last2,
                       })

    # Get user 1 and 2 tokens
    token1 = {"token": r1.json()["token"]}
    token2 = {"token": r2.json()["token"]}

    # User 1 creates a channel
    r3 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json={
                           **token1,
                           **{
                               "name": "Cowabunga",
                               "is_public": True
                           }
                       })
    ch_id1 = {"channel_id": r3.json()["channel_id"]}

    # User 2 joins the channel
    requests.post(f"{BASE_URL}/channel/join",
                  headers=HEADERS,
                  json={
                      **token2,
                      **ch_id1
                  })

    # User 1 sends a message
    r4 = requests.post(f"{BASE_URL}/message/send",
                       headers=HEADERS,
                       json={
                           **token1,
                           **ch_id1,
                           **{
                               "message": "This channel is cool",
                               "time_sent": time.time(),
                           },
                       })

    # Get msg ids
    msg_id1 = {"message_id": r4.json()["message_id"]}

    # User 2 attempts to edits user 1's message
    with pytest.raises(requests.RequestException):
        try_edit = {
            **token2,
            **msg_id1,
            **{
                "message": "This channel is not cool",
            },
        }
        requests.put(f"{BASE_URL}/message/edit",
                     headers=HEADERS,
                     json=try_edit).raise_for_status()

    # User 2 attempts to remove user 1's message
    with pytest.raises(requests.RequestException):
        try_rmv = {**token2, **msg_id1}
        requests.delete(f"{BASE_URL}/message/remove",
                        headers=HEADERS,
                        json=try_rmv).raise_for_status()


def test_message_send_later(get_new_user_detail_1):
    """
    Test message send later
    """
    # Get user 1
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    r1 = requests.post(f"{BASE_URL}/auth/register",
                       headers=HEADERS,
                       json={
                           "email": email1,
                           "password": password1,
                           "name_first": name_first1,
                           "name_last": name_last1,
                       })
    token1 = {"token": r1.json()["token"]}

    # User 1 creates a channel
    r3 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json={
                           **token1,
                           **{
                               "name": "Cowabunga",
                               "is_public": True
                           }
                       })
    ch_id1 = {"channel_id": r3.json()["channel_id"]}

    # User 1 sends a message for later
    r4 = requests.post(f"{BASE_URL}/message/sendlater",
                       headers=HEADERS,
                       json={
                           **token1,
                           **ch_id1,
                           **{
                               "message": "This channel is cool",
                               "time_sent": time.time() + 2,
                           },
                       })
    assert r4.status_code == requests.codes.ok

    # Get msg ids
    msg_id1 = {"message_id": r4.json()["message_id"]}

    # Check if message sent for later has been sent
    # TODO: LOGIC FOR CHECKING IF MESSAGE SENT LATER HAS SENT


def test_message_react(get_new_user_detail_1, get_new_user_detail_2):
    """
    Test message reacting and unreacting
    """
    # Get user 1 and 2 details
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    email2, password2, name_first2, name_last2 = get_new_user_detail_2

    # Register users 1 and 2
    r1 = requests.post(f"{BASE_URL}/auth/register",
                       headers=HEADERS,
                       json={
                           "email": email1,
                           "password": password1,
                           "name_first": name_first1,
                           "name_last": name_last1,
                       })
    r2 = requests.post(f"{BASE_URL}/auth/register",
                       headers=HEADERS,
                       json={
                           "email": email2,
                           "password": password2,
                           "name_first": name_first2,
                           "name_last": name_last2,
                       })

    # Get user 1 and 2 tokens
    token1 = {"token": r1.json()["token"]}
    token2 = {"token": r2.json()["token"]}

    # User 1 creates a channel
    r3 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json={
                           **token1,
                           **{
                               "name": "Cowabunga",
                               "is_public": True
                           }
                       })
    ch_id1 = {"channel_id": r3.json()["channel_id"]}

    # User 2 joins the channel
    requests.post(f"{BASE_URL}/channel/join",
                  headers=HEADERS,
                  json={
                      **token2,
                      **ch_id1
                  })

    # User 1 sends a message
    r4 = requests.post(f"{BASE_URL}/message/send",
                       headers=HEADERS,
                       json={
                           **token1,
                           **ch_id1,
                           **{
                               "message": "This channel is cool",
                               "time_sent": time.time(),
                           },
                       })

    # Get msg ids
    msg_id1 = {"message_id": r4.json()["message_id"]}

    # User 1 reacts to the message
    react1 = {**token1, **msg_id1, **{"react_id": 1}}
    r5 = requests.post(f"{BASE_URL}/message/react",
                       headers=HEADERS,
                       json=react1)
    assert r5.status_code == requests.codes.ok

    # User 2 reacts to the message
    react2 = {**token2, **msg_id1, **{"react_id": 1}}
    r6 = requests.post(f"{BASE_URL}/message/react",
                       headers=HEADERS,
                       json=react2)
    assert r6.status_code == requests.codes.ok

    # User 1 unreacts to the message
    react3 = {**token1, **msg_id1, **{"react_id": 0}}
    r7 = requests.post(f"{BASE_URL}/message/unreact",
                       headers=HEADERS,
                       json=react3)
    assert r7.status_code == requests.codes.ok

    # User 2 unreacts to the message
    react4 = {**token1, **msg_id1, **{"react_id": 0}}
    r8 = requests.post(f"{BASE_URL}/message/unreact",
                       headers=HEADERS,
                       json=react4)
    assert r8.status_code == requests.codes.ok


def test_message_pin(get_new_user_detail_1, get_new_user_detail_2):
    """
    Test message pinning and unpinning
    """
    # Get user 1 and 2 details
    email1, password1, name_first1, name_last1 = get_new_user_detail_1
    email2, password2, name_first2, name_last2 = get_new_user_detail_2

    # Register users 1 and 2
    r1 = requests.post(f"{BASE_URL}/auth/register",
                       headers=HEADERS,
                       json={
                           "email": email1,
                           "password": password1,
                           "name_first": name_first1,
                           "name_last": name_last1,
                       })
    r2 = requests.post(f"{BASE_URL}/auth/register",
                       headers=HEADERS,
                       json={
                           "email": email2,
                           "password": password2,
                           "name_first": name_first2,
                           "name_last": name_last2,
                       })

    # Get user 1 and 2 tokens
    token1 = {"token": r1.json()["token"]}
    token2 = {"token": r2.json()["token"]}

    # User 1 creates a channel
    r3 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json={
                           **token1,
                           **{
                               "name": "Cowabunga",
                               "is_public": True
                           }
                       })
    ch_id1 = {"channel_id": r3.json()["channel_id"]}

    # User 2 joins the channel
    requests.post(f"{BASE_URL}/channel/join",
                  headers=HEADERS,
                  json={
                      **token2,
                      **ch_id1
                  })

    # User 1 sends a message
    r4 = requests.post(f"{BASE_URL}/message/send",
                       headers=HEADERS,
                       json={
                           **token1,
                           **ch_id1,
                           **{
                               "message": "This channel is cool",
                               "time_sent": time.time(),
                           },
                       })

    # Get msg ids
    msg_id1 = {"message_id": r4.json()["message_id"]}

    # User 1 pins the message
    r5 = requests.post(f"{BASE_URL}/message/pin",
                       headers=HEADERS,
                       json={
                           **token1,
                           **msg_id1
                       })
    assert r5.status_code == requests.codes.ok

    # User 2 pinning the message raises InputError as message is already pinned
    with pytest.raises(requests.RequestException):
        requests.post(f"{BASE_URL}/message/pin",
                      headers=HEADERS,
                      json={
                          **token2,
                          **msg_id1
                      }).raise_for_status()

    # User 1 upins the message
    r7 = requests.post(f"{BASE_URL}/message/unpin",
                       headers=HEADERS,
                       json={
                           **token1,
                           **msg_id1
                       })
    assert r7.status_code == requests.codes.ok

    # User 2 pins the message
    r8 = requests.post(f"{BASE_URL}/message/unpin",
                       headers=HEADERS,
                       json={
                           **token2,
                           **msg_id1
                       })
    assert r7.status_code == requests.codes.ok
