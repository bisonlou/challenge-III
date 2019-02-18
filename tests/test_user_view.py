import unittest
from tests.test_base import TestBase
from api.models.user_model import User
from api.database.engine import DbConnection

base = TestBase()


class TestUserView(unittest.TestCase):

    def setUp(self):
        """
        Setup database connection
        """
        self.db_services = DbConnection()

    def tearDown(self):
        """
        teardown database
        """
        self.db_services.reset_database()

    def test_register_user_succesfuly(self):
        """
        Test registering a user succesfuly
        """    
        response = base.register_user()
        self.assertEqual(response.status_code, 201)

    def test_register_user_with_blank_password(self):
        """
        Test registering a user without a password
        """
        data = {'password': ''}
        response = base.register_user(data)

        self.assertEqual(response.status_code, 400)
   
    def test_register_user_with_blank_firstname(self):
        """
        Test registering a user with a blank first name
        """
        data = {'first_name': ''}
        response = base.register_user(data)

        self.assertEqual(response.status_code, 400)

    def test_register_with_long_password(self):
        """
        Test registering a user with password longer than 12 characters
        """
        data = {'password': 'Pa$$word123456'}
        response = base.register_user(data)

        self.assertEqual(response.status_code, 400)

    def test_register_with_long_invalid_email(self):
        """
        Test registering a user with an invalid email
        """
        data = {'email': 'bisonlou.com'}
        response = base.register_user(data)

        self.assertEqual(response.status_code, 400)

    def test_register_duplicate_user(self):
        """
        Test registering a user a second time
        """
        base.register_user()
        response = base.register_user()

        self.assertEqual(response.status_code, 409)

    def test_register_with_improper_type(self):
        """
        Test registering a user name 
        """
        data = {'user_name': 123}
        response = base.register_user(data)

        self.assertEqual(response.status_code, 400)

    def test_get_user(self):
        """
        Test getting one user
        """
        credentials = {'email': 'bisonlou@ireporter.com',
                       'password': 'Pa$$word123'}
        token = base.get_token(credentials)
        response = base.get_user(token)

        self.assertEqual(response.status_code, 200)

    def test_get_users_as_admin(self):
        """
        Test getting one user as admin
        """
        credentials = {'email': 'bisonlou@gmail.com',
                       'password': 'Pa$$word123'}

        token = base.get_token(credentials)
        response = base.get_user(token)

        self.assertEqual(response.status_code, 200)

    def test_get_users_as_admin(self):
        """
        Test getting users as admin
        """
        credentials = {'email': 'bisonlou@gmail.com',
                       'password': 'Pa$$word123'}

        token = base.get_token(credentials)
        response = base.get_users(token)

        self.assertEqual(response.status_code, 200)

    def test_get_users_as_non_admin(self):
        """
        Test getting users as non admin
        """
        credentials = {'email': 'bisonlou@ireporter.com',
                       'password': 'Pa$$word123'}

        token = base.get_token(credentials)
        response = base.get_users(token)

        self.assertEqual(response.status_code, 403)
    