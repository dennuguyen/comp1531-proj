"""
System testing module to assure general correctness of auth application systems
and http routes.

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
import json

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


def test_auth(get_new_user_detail_1):
    """
    Test the auth register, login, logout routes
    """
    # Get the user's data
    email, password, name_first, name_last = get_new_user_detail_1
    reg1 = {
        "email": email,
        "password": password,
        "name_first": name_first,
        "name_last": name_last,
    }

    # Register user 1
    r1 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS,
                       json=reg1)  # json= is equivalent to data=json.dumps()
    assert r1.status_code == requests.codes.ok

    u_id1 = r1.json()["u_id"]
    token1 = {"token": r1.json()["token"]}

    # Logging in user 1 is successful
    login1 = {"email": email, "password": password}
    r2 = requests.post(f"{BASE_URL}/auth/login", headers=HEADERS, json=login1)

    u_id2 = r2.json()["u_id"]
    token2 = {"token": r2.json()["token"]}

    # Confirm u_id for r1 and r2 are the same
    assert u_id1 == u_id2

    # Logout the user from session 1
    r3 = requests.post(f"{BASE_URL}/auth/logout", headers=HEADERS, json=token1)
    assert r3.status_code == requests.codes.ok

    # Logout the user from session 2
    r4 = requests.post(f"{BASE_URL}/auth/logout", headers=HEADERS, json=token2)
    assert r4.status_code == requests.codes.ok


def test_auth_register_exception_handling(get_new_user_detail_1):
    """
    Test the auth register exception handling
    """
    # Get the user's data
    email, password, name_first, name_last = get_new_user_detail_1
    reg1 = {
        "email": email,
        "password": password,
        "name_first": name_first,
        "name_last": name_last,
    }

    # Attempt a register with a too short password
    with pytest.raises(requests.RequestException):
        wrong_reg = {
            "email": email,
            "password": password[:5],
            "name_first": name_first,
            "name_last": name_last,
        }
        requests.post(f"{BASE_URL}/auth/register",
                      headers=HEADERS,
                      json=wrong_reg).raise_for_status()

    # Register user 1
    r1 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg1)
    assert r1.status_code == requests.codes.ok
    print(json.load(r1))
    assert 1 == 2

    # Attempting to register user 1 again will raise Exception due to already
    # registered email
    with pytest.raises(requests.RequestException):
        requests.post(f"{BASE_URL}/auth/register", headers=HEADERS,
                      json=reg1).raise_for_status()


def test_auth_login_exception_handling(get_new_user_detail_1):
    """
    Test the auth login and logout exception handling
    """
    # Get the user's data
    email, password, name_first, name_last = get_new_user_detail_1
    reg1 = {
        "email": email,
        "password": password,
        "name_first": name_first,
        "name_last": name_last,
    }

    # Register user 1
    r1 = requests.post(f"{BASE_URL}/auth/register", headers=HEADERS, json=reg1)
    assert r1.status_code == requests.codes.ok

    token1 = {"token": r1.json()["token"]}

    # Attempt login with incorrect password
    with pytest.raises(requests.RequestException):
        attempt1 = {"email": email, "password": password + "1"}
        requests.post(f"{BASE_URL}/auth/login", headers=HEADERS,
                      json=attempt1).raise_for_status()

    # Attempt login with incorrect email
    with pytest.raises(requests.RequestException):
        attempt2 = {"email": "prefix" + email, "password": password}
        requests.post(f"{BASE_URL}/auth/login", headers=HEADERS,
                      json=attempt2).raise_for_status()

    # Log out after a register should be possible as register logs user in
    r2 = requests.post(f"{BASE_URL}/auth/logout", headers=HEADERS, json=token1)
    assert r2.status_code == requests.codes.ok

    # Logout with same invalidated token returns False
    r3 = requests.post(f"{BASE_URL}/auth/logout", headers=HEADERS, json=token1)
    assert r3.json()["is_success"] == False
