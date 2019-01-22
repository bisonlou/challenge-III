import unittest
import json
from api import app, test_client
from api.models.user_model import User, UserServices


class TestUserView(unittest.TestCase):

    def setUp(self):
        """
        Setup test client
        """
        self.test_client = test_client   
        self.user_services = UserServices()         

    def tearDown(self):
        """
        teardown test client
        """
        self.user_services.remove_all()        

    def test_register_user_succesfuly(self):
        """
        Test registering a user succesfuly
        """
        user = {
            'user_name': 'bison',
            'email': 'bisonlou@gmail.com',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': 'innocent'
        }

        response = self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 201)

    def test_register_user_with_blank_password(self):
        """
        Test registering a user without a password
        """
        user = {
            'user_name': 'bison',
            'email': 'bisonlou@aol.com',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': '',
            'other_names': ''
        }

        response = self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertDictContainsSubset(
            {'length': 'Password should be between 6 and 12 characters'},
            message['data'])

    def test_register_user_with_missing_keys(self):
        """
        Test registering a user with missing email
        """
        user = {
            'user_name': 'bison',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': ''
        }

        response = self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

    def test_register_user_with_blank_firstname(self):
        """
        Test registering a user with a blank first name
        """
        user = {
            'user_name': 'bison',
            'email': 'bisonlou@gmail.com',
            'first_name': '',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': '',
            'other_names': ''
        }

        response = self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

    def test_register_with_long_password(self):
        """
        Test registering a user with password longer than 12 characters
        """
        user = {
            'user_name': 'bison',
            'email': 'bisonlou@gmail.com',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123456',
            'other_names': ''
        }

        response = self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertDictContainsSubset(
            {'length': 'Password should be between 6 and 12 characters'},
            message['data'])

    def test_register_with_long_invalid_email(self):
        """
        Test registering a user with an invalid email
        """
        user = {
            'user_name': 'bison',
            'email': 'bisonlougmail.com',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': 'innocent'
        }

        response = self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

    def test_register_duplicate_user(self):
        """
        Test registering a user a second time
        """
        user = {
            'user_name': 'bison',
            'email': 'bisonlou@gmail.com',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': 'innocent'
        }

        self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

        response = self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 409)

    def test_register_with_improper_type(self):
        """
        Test registering a user a second time
        """
        user = {
            'user_name': 123,
            'email': 'bisonlou@gmail.com',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': 'innocent'
        }

        self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

        response = self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 400)