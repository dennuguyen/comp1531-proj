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
import requests
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
    assert data.get_data().get_user_list() == []
    assert data.get_data().get_message_list() == []
    assert data.get_data().get_message_wait_list() == []
    assert data.get_data().get_channel_list() == []
    assert data.get_data().get_login_list() == []
    assert data.get_data().get_password_list() == []


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
    assert r3.status_code == requests.codes.ok  #TODO: 400 ERROR

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
    assert r7.status_code == requests.codes.ok

    # User 2 leaves second channel
    leave2 = {**token2, **ch_id2}
    r8 = requests.post(f"{BASE_URL}/channel/leave",
                       headers=HEADERS,
                       json=leave2)
    assert r8.status_code == requests.codes.ok


def test_channel_owner():
    pass


def test_channel_list():
    pass


def test_channel_messages():
    pass