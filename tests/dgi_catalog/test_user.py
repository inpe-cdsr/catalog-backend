# pylint: disable-msg=C0103

from unittest import TestCase
from json import loads, dumps

from dgi_catalog import app as dgi_catalog_app

from random import randrange
print(randrange(10))


app = dgi_catalog_app.test_client()

URL = '/catalog/user/'


class TestCatalogUser(TestCase):
    """
    TestCatalogUser
    """

    def test__post_delete__catalog_user__200_success(self):
        """
        TestCatalogUser.test__post__catalog_user__200_success

        Test the creation of a user
        """

        random_seed = randrange(9999999)

        email = 'test_user_{}@test_user.com'.format(random_seed)

        # 'addressId = 3' is a default address to test
        body = {
            'email': email, 'password': 'test', 'fullname': 'Test',
            'cnpjCpf': '123456', 'areaCode': '12', 'phone': '1452-2563', 'company': 'Abc',
            'companyType': '', 'activity': 'developer', 'addressId': 3,
            # 'userType': '', 'userStatus':  '', 'marlin': 0
        }

        response = app.post(URL, data=dumps(body))

        self.assertEqual(200, response.status_code)
        self.assertEqual(email, response.data.decode('utf-8'))

        # TODO: add delete user here


class TestCatalogUserError(TestCase):
    """
    TestCatalogUserError
    """

    def test__post__catalog_user__400_bad_request(self):
        """
        TestCatalogUserError.test__post__catalog_user__400_bad_request

        Test the creation of a user
        """

        # 'addressId = 3' is a default address to test
        body = {
            'email': 'test@localhost.com', 'password': 'test', 'fullname': 'Test',
            'cnpjCpf': '123456', 'areaCode': '12', 'phone': '1452-2563', 'company': 'Abc',
            'companyType': '', 'activity': 'developer',
            # 'userType': '',
            'addressId': 3,
            # 'userStatus':  '',
            # 'marlin': 0
        }

        response = app.post(URL, data=dumps(body))

        self.assertEqual(400, response.status_code)
        self.assertNotEqual("1062 (23000): Duplicate entry 'test_user@test_user.com' for key 'PRIMARY'",
                            loads(response.data))
