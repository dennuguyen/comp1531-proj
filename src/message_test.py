#Raymond: tests for message.py

from message import send
from message import remove
from message import edit
from message import check_message_is_valid
from message import check_token_is_valid
from message import check_user_is_member
from message import check_channel_id_is_valid
from message import check_if_authorised_user

#Test for message_send

def test_send_authorised_user():
    assert send(12345, 1, 'The quick brown fox jumps over the lazy dog.') == {'message_id' : 1}
    pass

def test_send_non_member():
    assert send(12345, 1, 'The quick brown fox jumps over the lazy dog.') != {'message_id' : 1}
    pass

def test_send_message_exceed_limit():
    assert send(12345, 1, 'Post no so what deal evil rent by real in. But her ready least set lived spite solid. September how men saw tolerably two behaviour arranging. She offices for highest and replied one venture pasture. Applauded no discovery in newspaper allowance am northward. Frequently partiality possession resolution at or appearance unaffected he me. Engaged its was evident pleased husband. Ye goodness felicity do disposal dwelling no. First am plate jokes to began of cause an scale. Subjects he prospect elegance followed no overcame possible it on. Resolution possession discovered surrounded advantages has but few add. Yet walls times spoil put. Be it reserved contempt rendered smallest. Studied to passage it mention calling believe an. Get ten horrible remember pleasure two vicinity. Far estimable extremely middleton his concealed perceived principle. Any nay pleasure entrance prepared her. On recommend tolerably my belonging or am. Mutual has cannot beauty indeed now sussex merely you. It possible') != {'message_id' : 1}
    pass

#Test for message_remove

def test_remove_existing_message():
    assert remove(12345, 1) == {}
    pass

def test_remove_non_existing_message():
    assert remove(12345, 1) != {}
    pass

def test_remove_non_authorised_user():
    assert remove (12345, 1) != {}
    pass

#Test for message_edit

def test_edit1():
    assert edit(12345, 1, 'The quick brown fox jumpes over the lazy dog.') == {}
    pass

#Test for general functions

def test_check_token_is_valid():
    assert check_token_is_valid(12345) == True
    pass

def test_check_message_is_valid():
    assert check_message_is_valid('Post no so what deal evil rent by real in. But her ready least set lived spite solid. September how men saw tolerably two behaviour arranging. She offices for highest and replied one venture pasture. Applauded no discovery in newspaper allowance am northward. Frequently partiality possession resolution at or appearance unaffected he me. Engaged its was evident pleased husband. Ye goodness felicity do disposal dwelling no. First am plate jokes to began of cause an scale. Subjects he prospect elegance followed no overcame possible it on. Resolution possession discovered surrounded advantages has but few add. Yet walls times spoil put. Be it reserved contempt rendered smallest. Studied to passage it mention calling believe an. Get ten horrible remember pleasure two vicinity. Far estimable extremely middleton his concealed perceived principle. Any nay pleasure entrance prepared her. On recommend tolerably my belonging or am. Mutual has cannot beauty indeed now sussex merely you. It possible') == False
    pass

def test_check_channel_id_is_valid():
    assert check_channel_id_is_valid(1) == True
    pass

def test_check_user_is_member():
    assert check_user_is_member(12345, 1) == True
    pass

def test_check_if_authorised_user():
    assert check_if_authorised_user (12345, 1) == True
    pass
