# web_based_asset_database/tests/test_app.py

import io
import os

import unittest
from app import app

class testApp(unittest.TestCase):

    #Setting up test_clienta and test config 
    def setUp(self):

        app.config['TESTING'] = True
        self.app = app.test_client()

    #Checking if index.html returns status code 200 = success
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        print(f"Index.html status = success")

    #Checking if addMesh.html returns status code 200 = success
    def test_addMesh(self):
        response = self.app.get('/addMesh.html')
        self.assertEqual(response.status_code, 200)
        print(f"addMesh.html status = success")

    #Checking if viewDatabase.html returns status code 200 = success
    def test_viewDatabase(self):
        response = self.app.get('/viewDatabase.html')
        self.assertEqual(response.status_code, 200)
        print(f"viewDatabase.html status = success")

    #Checking if non-exisiting page returns status code 404
    def test_failed(self):
        response = self.app.get('/failed')
        self.assertEqual(response.status_code, 404)
        print(f"Non-exisiting page status = failed")


if __name__ == '__main__':
    unittest.main()