from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        test_user = UserModel('test_guy', '123456')

        self.assertEqual(test_user.username, 'test_guy',
                         f"Mismatch between the expected value - test_guy - and the retrieved value, {test_user.username}")
        self.assertEqual(test_user.password, '123456',
                         f"Mistmatch between the expected password - 123456 - and the given password, {test_user.password}")
