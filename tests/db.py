from unittest import TestCase, main

from testutils import import_project_root, create_database
import_project_root()

from config import DB_CONNECTION

from queries import Message, GetMessages, AddMessages

class Messages(TestCase):
    @classmethod
    def setUpClass(cls):
        connection = create_database(DB_CONNECTION)
        cls._connection = connection

    def test_can_get_a_message(self):
        get_messages = GetMessages(self._connection)
        result = get_messages()
        self.assertEqual('irc', result[0].type)

    def test_can_add_a_message(self):
        add_messages = AddMessages(self._connection)
        messages = [Message('jabber', 'jabber.com', 'general@chat.jabber.com',
            'foo', 'mention', 'hey you, do a thing', 'html')]
        result = add_messages(messages)
        self.assertIsNotNone(result)
        # we return the id of the added messages
        self.assertIsInstance(result[0], int)



