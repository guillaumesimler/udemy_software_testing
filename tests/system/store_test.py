from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test_store')

                expected = {'name': 'test_store',
                            'items': []}

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 201)

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                response = client.post('/store/test_store')

                expected = {'message': "A store with name '{}' already exists.".format('test_store')}

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 400)

    def test_deleting_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test_store')
                self.assertEqual(response.status_code, 201, "The store ought to be created")

                response = client.delete('/store/test_store')
                expected = {'message': 'Store deleted'}
                self.assertDictEqual(json.loads(response.data), expected)

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                response = client.get('/store/test_store')

                expected = {'name': 'test_store',
                            'items': []}

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 200)

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test_store')

                expected = {'message': 'Store not found'}

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 404)

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')

                item1 = ItemModel('item1', 99.9, 1)
                item2 = ItemModel('item2', 19.9, 1)

                item1.save_to_db()
                item2.save_to_db()

                expected = {'name': 'test_store',
                            'items': [{'name': 'item1', 'price': 99.9},
                                      {'name': 'item2', 'price': 19.9}]}

                response = client.get('/store/test_store')

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 200)

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                client.post('/store/test_store2')

                expected = {'stores': [
                                {'name': 'test_store', 'items': []},
                                {'name': 'test_store2', 'items': []}
                ]}

                response = client.get('/stores')

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 200)

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                client.post('/store/test_store2')

                item1 = ItemModel('item1', 99.9, 1)
                item2 = ItemModel('item2', 19.9, 2)

                item1.save_to_db()
                item2.save_to_db()

                expected = {'stores': [
                    {'name': 'test_store', 'items': [{'name': 'item1', 'price': 99.9}]},
                    {'name': 'test_store2', 'items': [{'name': 'item2', 'price': 19.9}]}
                ]}

                response = client.get('/stores')

                self.assertDictEqual(json.loads(response.data), expected)
                self.assertEqual(response.status_code, 200)
