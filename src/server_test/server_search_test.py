"""
System testing module to assure general correctness of server application
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

BASE_URL = "http://127.0.0.1:20000"
HEADERS = {"Content-Type": "application/json"}


@pytest.fixture(autouse=True)
def reset_state():
    """
    This pytest fixture automatically runs for every test function call
    """
    r = requests.post(f"{BASE_URL}/workspace/reset")
    assert r.status_code == requests.codes.ok


def test_search(get_new_user_detail_1):
    """
    Test the auth register exception handling
    """
    # Register user 1
    email, password, name_first, name_last = get_new_user_detail_1
    r1 = requests.post(
        f"{BASE_URL}/auth/register",
        headers=HEADERS,
        json={
            "email": email,
            "password": password,
            "name_first": name_first,
            "name_last": name_last,
        },
    )
    token = {"token": r1.json()["token"]}

    # User 1 creates a channel
    r2 = requests.post(
        f"{BASE_URL}/channels/create",
        headers=HEADERS,
        json={
            **token,
            **{
                "name": "Cowabunga",
                "is_public": True,
            },
        },
    )
    ch_id = {"channel_id": r2.json()["channel_id"]}

    # Send a message
    r3 = requests.post(
        f"{BASE_URL}/message/send",
        headers=HEADERS,
        json={
            **token,
            **ch_id,
            **{
                "message": "This channel is cool",
                "time_sent": time.time(),
            },
        },
    )

    # Search for a message
    srch = {
        **token,
        **{
            "query_str": "This",
        },
    }
    r4 = requests.get(
        f"{BASE_URL}/search",
        headers=HEADERS,
        params=srch,
    )

    assert r4.json()['messages'][0]['message'] == 'This channel is cool'
    assert r4.status_code == requests.codes.ok

        # Search for another message
    srch = {
        **token,
        **{
            "query_str": "This is Star Trek Enterprise",
        },
    }
    r4 = requests.get(
        f"{BASE_URL}/search",
        headers=HEADERS,
        params=srch,
    )
    
    assert r4.json()['messages'] == []
    assert r4.status_code == requests.codes.ok


    # TODO: MORE EXTENSIVE TESTS
