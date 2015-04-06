from unittest import TestCase, main

from config import DB_CONNECTION

from testutils import import_project_root, create_database
import_project_root()

import website
import os
import tempfile

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
