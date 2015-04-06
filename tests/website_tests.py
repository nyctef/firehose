from unittest import TestCase, main
from mock import patch, Mock

from config import DB_CONNECTION

from testutils import import_project_root, create_database
import_project_root()

import website
import os
import tempfile
import json

from queries import Message

new_message_data = json.dumps({
    'source': 1,
    'body': 'a message body',
    'format': 'plain',
    })

class FakeGetMessages:
    def __init__(self, connection):
        pass
    def __call__(self):
        return [Message('irc', 'freenode.net', '#chat', 'someguy', 'normal',
            'a_message', 'plain'),
                Message('irc', 'freenode.net', '#chat', 'someguy', 'normal',
            'message_2', 'plain')]

class FakeAddMessage:
    def __init__(self, connection):
        pass
    def __call__(self, messages):
        assert len(messages) == 1
        assert type(messages[0].source.id) is int
        assert messages[0].body is not None
        return [1]


class Website(TestCase):

    def setUp(self):
        #self._connection = create_database(DB_CONNECTION)
        website.app.config['TESTING'] = True
        self.app = website.app.test_client()

    def tearDown(self):
        #self._connection.close()
        pass

    def test_index_does_not_404(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert 'firehose' in response.data

    def test_index_displays_some_messages(self):
        website.deps.get_connection = lambda: None
        website.deps.GetMessages = FakeGetMessages
        response = self.app.get('/')
        assert 'message_2' in response.data

    def test_post_to_messages_creates_new_message(self):
        website.deps.get_connection = lambda: None
        website.deps.AddMessages = FakeAddMessage
        response = self.app.post('/messages', data=new_message_data)
        assert response.status_code == 201 # created
        assert response.headers['location'].endswith('/messages/1')
