from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
import json

from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '123456').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '123456'}),
                                           headers={'Content-Type': 'application/json'})

                auth_token = json.loads(auth_request.data)['access_token']
                self.auth_header = {'Authorization': f'JWT {auth_token}'}

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers=self.auth_header)

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Item not found'})

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 99.99, 1).save_to_db()
                resp = client.get('/item/test_item', headers=self.auth_header)

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_item',
                                                             'price': 99.99})

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                resp = client.post('/item/test_item', data={'price': 99.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_item',
                                                             'price': 99.99})

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 39.99, 1).save_to_db()
                resp = client.post('/item/test_item', data={'price': 99.99, 'store_id': 1})

                expected = {'message': "An item with name 'test_item' already exists."}
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(json.loads(resp.data), expected)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 99.99, 1).save_to_db()
                resp = client.delete('/item/test_item')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Item deleted'})

    def test_modify_existing_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 39.99, 1).save_to_db()
                resp = client.put('/item/test_item', data={'price': 99.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_item',
                                                             'price': 99.99})

    def test_modify_new_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 39.99, 1).save_to_db()
                resp = client.put('/item/test_item2', data={'price': 99.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_item2',
                                                             'price': 99.99})

    def test_get_items_empty(self):
        pass

    def test_get_items(self):
        pass
