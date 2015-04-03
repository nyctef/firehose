from unittest import TestCase, main

from testutils import import_project_root, create_database
import_project_root()

from config import DB_CONNECTION

from queries import GetMessages

class Messages(TestCase):
    @classmethod
    def setUpClass(cls):
        connection = create_database(DB_CONNECTION)
        cls._connection = connection

    def test_can_get_a_message(self):
        get_messages = GetMessages(self._connection)
        result = get_messages()
        self.assertEqual('irc', result[0].type)



