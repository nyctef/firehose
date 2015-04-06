from unittest import TestCase, main

from config import DB_CONNECTION

from testutils import import_project_root, create_database
import_project_root()
from queries import Message, MessageSource, GetMessages, AddMessages
from db import wait_for_notify
from gevent import queue, spawn, sleep
import psycopg2

class Messages(TestCase):
    @classmethod
    def setUpClass(cls):
        connection = create_database(DB_CONNECTION)
        cls._connection = connection

    def test_can_get_a_message(self):
        get_messages = GetMessages(self._connection)
        result = get_messages()
        self.assertEqual('irc', result[0].source.type)

    def test_can_add_a_message(self):
        add_messages = AddMessages(self._connection)
        messages = [Message(MessageSource(1,None,None,None),
            -1, 'general', 'foo', 'mention', 'hey you, do a thing', 'html')]
        result = add_messages(messages)
        self.assertIsNotNone(result)
        # we return the id of the added messages
        self.assertIsInstance(result[0], int)

    def test_notifies_get_added_to_queue(self):
        q = queue.Queue()
        conn1 = self._connection
        conn2 = psycopg2.connect(DB_CONNECTION)
        thread = spawn(wait_for_notify, conn2, q, 'test_notification')
        sleep() # let the notify thread start listening
        conn1.cursor().execute('''
        notify test_notification;
        ''')
        conn1.commit()
        self.assertIsNotNone(q.get())
        thread.kill()

