#Raymond: tests for message.py

import sys
sys.path.append('../src/')
import message

def test_send():
    assert message.send(12345, 1, 'The quick brown fox jumps over the lazy dog.') == {'message_id' : 1}

