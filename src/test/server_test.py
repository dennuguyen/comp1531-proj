import json
import urllib
import pytest
import sys
sys.path.append('../')
import server
import data
BASE_URL = "http://127.0.0.1:8080/"
HEADERS = {'Content-Type': 'application/json'}


@pytest.fixture(autouse=True)
def reset_state():
    """
    This pytest fixture automatically runs for every test function call
    """
    req_obj = urllib.request.Request(f"{BASE_URL}/workspace/reset",
                                     headers=HEADERS,
                                     method="POST")
    urllib.request.urlopen(req_obj)


def test_register(get_new_user_detail_1):
    """
    Test the register route
    """
    # Register the user
    #
    # Get the user's data
    email, password, name_first, name_last = get_new_user_detail_1
    send_reg = json.dumps({
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
    }).encode('utf-8')

    # Send data request
    request_obj = urllib.request.Request(f"{BASE_URL}/auth/register",
                                         data=send_reg,
                                         headers=HEADERS,
                                         method='POST')

    # Assert the payload
    payload = json.load(urllib.request.urlopen(request_obj))
    u_id = data.get_data().get_user_with_email(email).get_u_id()
    assert payload == data.get_data().get_login_with_u_id(
        u_id)[0].get_login_dict()

    # Logging in the user after register should be successful
    send_login = json.dumps({
        'email': email,
        'password': password,
    }).encode('utf-8')

    request_obj = urllib.request.Request(f"{BASE_URL}/auth/login",
                                         data=send_login,
                                         headers=HEADERS,
                                         method='POST')
    payload = json.load(urllib.request.urlopen(request_obj))
    assert payload == data.get_data().get_login_with_u_id(
        u_id)[1].get_login_dict()


# def test_login(get_new_user_detail_1):
#     """
#     Test the user login without a registered email
#     """
#     # Get the user's data
#     email, password, _, _ = get_new_user_detail_1
#     deliver = json.dumps({
#         'email': email,
#         'password': password
#     }).encode('utf-8')

#     # Send data request
#     req_obj = urllib.request.Request(f"{BASE_URL}/auth/login",
#                                      data=deliver,
#                                      headers=HEADERS,
#                                      method='POST')

#     payload = json.load(urllib.request.urlopen(req_obj))
#     assert payload == data.get_data().get_login_with_email(
#         email).get_login_dict()

# def test_logout():
#     """
#     Test the case of adding a single name and listing
#     """
#     # Add a John Doe via the /name/add route
#     data = json.dumps({'name': 'John Doe'}).encode('utf-8')
#     headers = {'Content-Type': 'application/json'}
#     req_obj = urllib.request.Request(f"{BASE_URL}/name/add",
#                                      data=data,
#                                      headers=headers,
#                                      method='POST')

#     # Successful name add returns empty dictionary
#     assert json.load(urllib.request.urlopen(req_obj)) == {}

#     # Check the payload
#     payload = json.load(urllib.request.urlopen(f"{BASE_URL}/name"))
#     assert payload == {'name': ['John Doe']}

# def test_add_name_multiple():
#     """
#     Test the case of adding multiple names and listing it
#     """
#     # Add a John Doe via the /name/add route
#     data1 = json.dumps({'name': 'John Doe'}).encode('utf-8')
#     headers = {'Content-Type': 'application/json'}
#     req_obj1 = urllib.request.Request(f"{BASE_URL}/name/add",
#                                       data=data1,
#                                       headers=headers,
#                                       method='POST')

#     # Successful name add returns empty dictionary
#     assert json.load(urllib.request.urlopen(req_obj1)) == {}

#     # Add second person
#     data2 = json.dumps({'name': 'Max Powers'}).encode('utf-8')
#     req_obj2 = urllib.request.Request(f"{BASE_URL}/name/add",
#                                       data=data2,
#                                       headers=headers,
#                                       method='POST')

#     # Successful name add returns empty dictionary
#     assert json.load(urllib.request.urlopen(req_obj2)) == {}

#     # Check the payload
#     payload = json.load(urllib.request.urlopen(f"{BASE_URL}/name"))
#     assert payload == {'name': ['John Doe', 'Max Powers']}

# def test_add_name_repeated():
#     """
#     Test the case of adding the same name multiple times
#     """
#     # Add a John Doe via the /name/add route
#     data1 = json.dumps({'name': 'John Doe'}).encode('utf-8')
#     headers = {'Content-Type': 'application/json'}
#     req_obj1 = urllib.request.Request(f"{BASE_URL}/name/add",
#                                       data=data1,
#                                       headers=headers,
#                                       method='POST')

#     # Successful name add returns empty dictionary
#     assert json.load(urllib.request.urlopen(req_obj1)) == {}

#     # Add second person
#     data2 = json.dumps({'name': 'John Doe'}).encode('utf-8')
#     req_obj2 = urllib.request.Request(f"{BASE_URL}/name/add",
#                                       data=data2,
#                                       headers=headers,
#                                       method='POST')

#     # Successful name add returns empty dictionary
#     assert json.load(urllib.request.urlopen(req_obj2)) == {}

#     # Check the payload
#     payload = json.load(urllib.request.urlopen(f"{BASE_URL}/name"))
#     assert payload == {'name': ['John Doe', 'John Doe']}

# def test_remove_name_once():
#     """
#     Test the removal of the name once
#     """
#     # Add a John Doe via the /name/add route
#     data1 = json.dumps({'name': 'John Doe'}).encode('utf-8')
#     headers = {'Content-Type': 'application/json'}
#     req_obj1 = urllib.request.Request(f"{BASE_URL}/name/add",
#                                       data=data1,
#                                       headers=headers,
#                                       method='POST')

#     # Open the URL to add the name
#     json.load(urllib.request.urlopen(req_obj1))

#     data2 = json.dumps({'name': 'John Doe'}).encode('utf-8')
#     req_obj2 = urllib.request.Request(f"{BASE_URL}/name/remove",
#                                       data=data2,
#                                       headers=headers,
#                                       method='DELETE')

#     # Successful name removal returns empty dictionary
#     assert json.load(urllib.request.urlopen(req_obj2)) == {}

#     # Check the payload
#     payload = json.load(urllib.request.urlopen(f"{BASE_URL}/name"))
#     assert payload == {'name': []}

# def test_remove_name_repeated():
#     """
#     Test removal of a name that was repeated which should only remove it once
#     """
#     # Add a John Doe via the /name/add route
#     data1 = json.dumps({'name': 'John Doe'}).encode('utf-8')
#     headers = {'Content-Type': 'application/json'}
#     req_obj1 = urllib.request.Request(f"{BASE_URL}/name/add",
#                                       data=data1,
#                                       headers=headers,
#                                       method='POST')

#     # Open the URL twice to add the name twice
#     json.load(urllib.request.urlopen(req_obj1))
#     json.load(urllib.request.urlopen(req_obj1))

#     data2 = json.dumps({'name': 'John Doe'}).encode('utf-8')
#     req_obj2 = urllib.request.Request(f"{BASE_URL}/name/remove",
#                                       data=data2,
#                                       headers=headers,
#                                       method='DELETE')

#     # Successful name removal returns empty dictionary
#     assert json.load(urllib.request.urlopen(req_obj2)) == {}

#     # Check the payload
#     payload = json.load(urllib.request.urlopen(f"{BASE_URL}/name"))
#     assert payload == {'name': ['John Doe']}

# def test_remove_empty():
#     """
#     Test removing an empty dictionary
#     """
#     data = json.dumps({'name': 'John Doe'}).encode('utf-8')
#     headers = {'Content-Type': 'application/json'}
#     req_obj = urllib.request.Request(f"{BASE_URL}/name/remove",
#                                      data=data,
#                                      headers=headers,
#                                      method='DELETE')

#     # Exception should raise on removal of empty list
#     with pytest.raises(Exception):
#         json.load(urllib.request.urlopen(req_obj))
