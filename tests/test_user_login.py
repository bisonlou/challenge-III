import unittest
from api.models.user_model import User
from api.database.engine import DbConnection
from tests.test_base import TestBase

base = TestBase()


class TestUserView(unittest.TestCase):

    def setUp(self):
        """
        Setup db services
        """
        self.db_services = DbConnection()

    def tearDown(self):
        """
        teardown test client
        """
        self.db_services.reset_database()      

    def test_login(self):
        """
        Test registering a user successfuly
        """
        credentials = {'email': 'bisonlou@gmail.com',
                       'password': 'Pa$$word123'}

        response = base.login_user(credentials)
        self.assertEqual(response.status_code, 200)

    def test_login_with_missing_data(self):
        """
        Test loging in without specifying a password
        """
        credentials = {'email': 'bisonlou@gmail.com'}

        response = base.login_user(credentials)
        self.assertEqual(response.status_code, 400)

    def test_login_with_empty_email(self):
        """
        Test login without an email
        """
        credentials = {'email': '',
                'password': 'Pa$$word123'}

        response = base.login_user(credentials)
        self.assertEqual(response.status_code, 400)

    def test_login_with_empty_password(self):
        """
        Test login with empty password
        """
        credentials = {'email': 'bisonlou@gmail.com',
                       'password': ''}

        response = base.login_user(credentials)
        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong_password(self):
        """
        Test login with wrong password
        """
        credentials = {'email': 'bisonlou@gmail.com',
                       'password': 'Password123'}

        response = base.login_user(credentials)
        self.assertEqual(response.status_code, 401)

    def test_login_with_wrong_email(self):
        """
        Test login with wrong email
        """
        credentials = {'email': 'bisonlou@abc.com',
                       'password': 'Pa$$word123'}

        response = base.login_user(credentials)
        self.assertEqual(response.status_code, 401)
    