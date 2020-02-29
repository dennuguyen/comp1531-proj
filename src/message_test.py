#Raymond: tests for message.py

from message import send
from message import remove
from message import edit

def test_send():
    assert send(12345, 1, 'The quick brown fox jumps over the lazy dog.') == {'message_id' : 1}
    pass

def test_remove():
    assert remove(12345, 1) == {}
    pass

def test_edit():
    assert edit(12345, 1, 'The quick brown fox jumpes over the lazy dog.') == {}
    pass
