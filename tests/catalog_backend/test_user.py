# pylint: disable-msg=C0103

from json import loads, dumps
from random import randrange
from unittest import TestCase

from catalog_backend import app as catalog_backend_app


catalog_backend_app.testing = True
app = catalog_backend_app.test_client()

URL = '/api/user/'
URL_LOGIN = '/api/auth/login'


class TestCatalogUser(TestCase):
    """TestCatalogUser"""

    def test__post_delete__catalog_user__200_success(self):
        """
        TestCatalogUser.test__post_delete__catalog_user__200_success

        Test the user creation and deletion
        """

        random_number = randrange(9999999)

        email = 'test_user_{}@test_user.com'.format(random_number)
        password = 'test'

        ##################################################
        # Create a user
        ##################################################

        # 'addressId = 3' is a default address to test
        body = {
            'email': email, 'password': password, 'fullname': 'Test',
            'cnpjCpf': '123456', 'areaCode': '12', 'phone': '1452-2563',
            'company': 'Abc', 'companyType': 'image processing',
            'activity': 'developer', 'addressId': 3,
            #'userType': '', 'userStatus':  '', 'marlin': 0
        }

        response = app.post(URL, data=dumps(body))

        expected = {
            'user_id': email
        }

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, loads(response.data.decode('utf-8')))

        ##################################################
        # Log the user in the system
        ##################################################

        body = {'email': email, 'password': password}

        response = app.post(URL_LOGIN, data=dumps(body))

        user_information = loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)

        ##################################################
        # Delete the user
        ##################################################

        authorization = 'Basic: ' + user_information['access_token']

        response = app.delete(URL + email, data=dumps(body),
                              headers={'Authorization': authorization})

        self.assertEqual(200, response.status_code)


class TestCatalogUserError(TestCase):
    """TestCatalogUserError"""

    def test__post__catalog_user__400_bad_request(self):
        """
        TestCatalogUserError.test__post__catalog_user__400_bad_request

        Test the user creation
        """

        # 'addressId = 3' is a default address to test
        body = {
            'email': 'test@localhost.com', 'password': 'test',
            'fullname': 'Test', 'cnpjCpf': '123456', 'areaCode': '12',
            'phone': '1452-2563', 'company': 'Abc', 'companyType': '',
            'activity': 'developer', 'addressId': 3,
            # 'userType': '', 'userStatus':  '', 'marlin': 0
        }

        response = app.post(URL, data=dumps(body))

        self.assertEqual(400, response.status_code)
        self.assertNotEqual(
            "1062 (23000): Duplicate entry 'test_user@test_user.com' for key 'PRIMARY'",
            loads(response.data)
        )
