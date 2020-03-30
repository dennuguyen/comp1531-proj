"""
System testing module to assure general correctness of channel application
systems and http routes.

Black box testing is used as the functionality of the application's systems are
already covered with unit testing. Therefore it can be considered that these
tests are more concerned about the end-user's experience.

Requests Module Documentation:
https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
"""
import server
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

def test_channels_create(get_new_user_detail_1, get_new_user_detail_2, get_new_user_detail_3):

    """
    Test channel creation
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

    # User 2 creates a channels
    ch2 = {**token2, **{"name": "Pizzaaa", "is_public": True}}
    r5 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json=ch2)
    assert r5.status_code == requests.codes.ok    

def test_channel_list(get_new_user_detail_1, get_new_user_detail_2, get_new_user_detail_3):

    """
    Test channel list and listall
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

    # User 2 creates a channels
    ch2 = {**token2, **{"name": "Pizzaaa", "is_public": True}}
    r5 = requests.post(f"{BASE_URL}/channels/create",
                       headers=HEADERS,
                       json=ch2)
    assert r5.status_code == requests.codes.ok    

    # Get the channel ids
    ch_id1 = {"channel_id": r4.json()["channel_id"]}
    ch_id2 = {"channel_id": r5.json()["channel_id"]}
    pass

    # User 2 joins first channel
    join1 = {**token2, **ch_id1}
    r6 = requests.post(f"{BASE_URL}/channel/join",
                       headers=HEADERS,
                       json=join1)
    assert r6.status_code == requests.codes.ok

    # User 3 joins first channel
    join2 = {**token3, **ch_id2}
    r7 = requests.post(f"{BASE_URL}/channel/join",
                       headers=HEADERS,
                       json=join2)
    assert r7.status_code == requests.codes.ok

    # User 2 calls channel list
    list1 = {**token2}
    r8 = requests.get(f"{BASE_URL}/channels/list",
                       list1)
    assert r8.status_code == requests.codes.ok 

        # User 2 calls channel list all
    listall1 = {**token2}
    r9 = requests.get(f"{BASE_URL}/channels/listall",
                       listall1)
    assert r9.status_code == requests.codes.ok 

        # User 3 calls channel list
    list2 = {**token3}
    r10 = requests.get(f"{BASE_URL}/channels/list",
                       list2)
    assert r10.status_code == requests.codes.ok 

        # User 3 calls channel list all
    listall2 = {**token3}
    r11 = requests.get(f"{BASE_URL}/channels/listall",
                       listall2)
    assert r11.status_code == requests.codes.ok 


