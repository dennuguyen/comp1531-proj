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

BASE_URL = "http://127.0.0.1:8080"
HEADERS = {"Content-Type": "application/json"}


@pytest.fixture(autouse=True)
def reset_state():
    """
    This pytest fixture automatically runs for every test function call
    """
    r = requests.post(f"{BASE_URL}/workspace/reset")
    assert r.status_code == requests.codes.ok


def test_user_profile(get_new_user_detail_1, get_new_user_detail_2):
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

    u_id1 = {"u_id": r1.json()['u_id']}
    u_id2 = {"u_id": r2.json()['u_id']}

    info1 = {**token1, **u_id1}
    info2 = {**token2, **u_id2}

    r3 = requests.get(f"{BASE_URL}/user/profile",info1)

    assert r3.json()['user']['u_id'] == r1.json()['u_id']
    assert r3.status_code == requests.codes.ok

    r4 = requests.get(f"{BASE_URL}/user/profile",info2)
    assert r4.json()['user']['u_id'] == r2.json()['u_id']
    assert r4.status_code == requests.codes.ok

    
