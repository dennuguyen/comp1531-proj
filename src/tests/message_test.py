#Raymond: tests for message.py

def test_send():
    assert send(12345, 1, 'The quick brown fox jumps over the lazy dog.') == {'message_id' : 1}

