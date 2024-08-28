import os
import tempfile
import unittest

from Core import Connection
from Core.Functions import create_new_database


class TestDatabaseConnect(unittest.TestCase):
    """create a temporary directory for all test to store data"""

    @classmethod
    def setUpClass(cls):
        cls.dir_name = tempfile.TemporaryDirectory()
        print(cls.dir_name)

    """cleanup the temporary directory"""

    @classmethod
    def tearDownClass(cls):
        cls.dir_name.cleanup()

    def test_create(self):
        # create an empty clutter base
        db_name = f"{self.dir_name.name}/test.db"
        self.assertTrue(create_new_database(db_name))
        # this should fail permission denied
        self.assertFalse(create_new_database("/usr/libtest.db"))

    def test_connect(self):
        self.assertTrue(create_new_database(f"{self.dir_name.name}/connect_test.db"))

        with Connection.MeshesConnection(
                f"{self.dir_name.name}/connect_test.db"
        ) as connection:
            self.assertTrue(connection != None)

        db = Connection.MeshesConnection(f"{self.dir_name.name}/connect_test.db")
        db.open()
        self.assertTrue(db.connection != None)
        db.close()

    def test_add_item(self):
        self.assertTrue(create_new_database("connect_test.db"))
        with Connection.MeshesConnection("connect_test.db") as connection:
            self.assertTrue(connection != None)
            connection.add_item(
                "./mesh/Cube.obj",
                "Cube",
                "obj",
                "me",
                "test",
                "01/01/2024"
            )