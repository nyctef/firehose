from unittest import TestCase, main

from testutils import import_project_root, create_database
import_project_root()

from queries import GetMessages

class Messages(TestCase):
    @classmethod
    def setUpClass(cls):
        print('creating database...')
        connection = None
        create_database(connection)
        cls._connection = connection

    def test_can_get_a_message(self):
        get_messages = GetMessages(self._connection)
        result = get_messages()
        self.assertIsNotNone(result[0])



