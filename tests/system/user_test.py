from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/register', data={'username': 'test', 'password': '123456'})

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'The new user was successfully created'}, json.loads(request.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '123456'})
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '123456'}),
                                           headers={'Content-Type': 'application/json'})
                self.assertIn('access_token', json.loads(auth_request.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '123456'})
                response = client.post('/register', data={'username': 'test', 'password': '123456'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'A user with that username already exists'})
