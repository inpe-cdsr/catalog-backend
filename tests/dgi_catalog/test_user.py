# pylint: disable-msg=C0103

from unittest import TestCase
from json import loads, dumps
from random import randrange

from dgi_catalog import app as dgi_catalog_app


app = dgi_catalog_app.test_client()

URL = '/catalog/user/'
URL_LOGIN = '/catalog/auth/login'


class TestCatalogUser(TestCase):
    """
    TestCatalogUser
    """

    def test__post_delete__catalog_user__200_success(self):
        """
        TestCatalogUser.test__post_delete__catalog_user__200_success

        Test the creation and deletion of a user
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
            'cnpjCpf': '123456', 'areaCode': '12', 'phone': '1452-2563', 'company': 'Abc',
            'companyType': '', 'activity': 'developer', 'addressId': 3,
            # 'userType': '', 'userStatus':  '', 'marlin': 0
        }

        response = app.post(URL, data=dumps(body))

        self.assertEqual(200, response.status_code)
        self.assertEqual(email, response.data.decode('utf-8'))

        ##################################################
        # Log the user in the system
        ##################################################

        body = { 'email': email, 'password': password }

        response = app.post(URL_LOGIN, data=dumps(body))

        token = response.data.decode('utf-8')

        self.assertEqual(200, response.status_code)
        # check if a non-empty string has been returned (i.e. a token has been returned)
        self.assertNotEqual('', token)

        ##################################################
        # Delete the user
        ##################################################

        authorization = 'Basic: ' + token

        response = app.delete(URL + email, data=dumps(body), headers={'Authorization': authorization})

        self.assertEqual(200, response.status_code)


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
