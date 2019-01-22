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

    def tearDown(self):
        """
        teardown test client
        """
        self.user_services.remove_all()        

    def test_login(self):
        """
        Test registering a user without a password
        """
        user = {
            'email': 'bisonlou@gmail.com',
            'password': 'Pa$$word123'
        }

        response = self.test_client.post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user))

        self.assertEqual(response.status_code, 200)

    def test_login_with_missing_data(self):
        """
        Test loging in withou specifying a password
        """
        user = {
            'email': 'bisonlou@gmail.com'
        }

        response = self.test_client.post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user))

        self.assertEqual(response.status_code, 400)

    def test_login_with_empty_email(self):
        """
        Test login without email
        """
        user = {
            'email': '',
            'password': 'Pa$$word123'
        }

        response = self.test_client.post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user))

        self.assertEqual(response.status_code, 400)

    def test_login_with_empty_password(self):
        """
        Test login with empty password
        """
        user = {
            'email': 'bisonlou@gmail.com',
            'password': ''
        }

        response = self.test_client.post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user))

        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong_password(self):
        """
        Test login with wrong password
        """
        user = {
            'email': 'bisonlou@gmail.com',
            'password': 'Password123'
        }

        response = self.test_client.post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user))

        self.assertEqual(response.status_code, 401)

    def test_login_with_wrong_email(self):
        """
        Test login with wrong email
        """
        user = {
            'email': 'bisonlou@outlook.com',
            'password': 'Pa$$word123'
        }

        response = self.test_client.post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 401)