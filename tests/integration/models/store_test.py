from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest

class StoreTest(BaseTest):

    def test_create_store_items_empty(self):
        store = StoreModel('test_store')

        self.assertListEqual(store.items.all(), [], "the newly create store should have no items, but has.")

    def test_crud(self):

        with self.app_context():
            store = StoreModel('test_store')

            self.assertIsNone(StoreModel.find_by_name('test_store'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test_store'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test_store'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 19.99,1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_json(self):

        store = StoreModel('test')

        expected = {'name' : 'test',
                    'items' : []}

        self.assertDictEqual(store.json(), expected)

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {'name': 'test_store',
                        'items': [{'name': 'test_item', 'price': 19.99}]}

            self.assertDictEqual(store.json(), expected)
