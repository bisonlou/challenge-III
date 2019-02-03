import unittest
import json
from api import app, test_client
from api.models.db import DbConnection


class TestRedFlagView(unittest.TestCase):

    def setUp(self):
        """
        Setup test client
        """
        self.test_client = test_client
        self.db_services = DbConnection()

        user_1 = {
            'user_name': 'bison',
            'email': 'bisonlou@aol.com',
            'date_registered': '2019-01-01',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': '',
            'is_admin': True
        }

        user_2 = {
            'user_name': 'bison',
            'email': 'bisonlou@yahoo.com',
            'date_registered': '2019-01-01',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': '',
            'is_admin': False
        }

        self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user_1)
        )

        self.test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user_2)
        )

        user1_login = {
            'email': 'bisonlou@aol.com',
            'password': 'Pa$$word123'
        }

        user2_login = {
            'email': 'bisonlou@yahoo.com',
            'password': 'Pa$$word123'
        }

        response_1 = self.test_client.post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user1_login)
        )

        response_2 = self.test_client.post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(user2_login)
        )

        self.admin_token = json.loads(
                           response_1.data)['data'][0]['access_token']
        self.non_admin_token = json.loads(
                               response_2.data)['data'][0]['access_token']

        red_flag_1 = {
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'status': 'pending',
            'images': ['photo_0979.jpg', 'photo_0094.jpg'],
            'videos': ['video_0002.mov']
        }

        red_flag_2 = {
            'title': 'Magistrate',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'status': 'pending',
            'images': ['photo_0979.jpg'],
            'videos': ['video_0002.mov']
        }

        self.test_client.post(
            '/api/v1/incidents',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token},
            content_type='application/json',
            data=json.dumps(red_flag_1)
        )

        self.test_client.post(
            '/api/v1/incidents',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token},
            content_type='application/json',
            data=json.dumps(red_flag_2)
        )

    def tearDown(self):
        """
        teardown test client
        """
        self.db_services.delete_all_incidents()
        self.db_services.delete_all_users()

    def test_add_proper_red_flag(self):
        """
        Test adding a red flag with expected keys
        Expect 201
        """
        red_flag = {
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'status': 'pending',
            'images': ['photo_0912.jpg'],
            'videos': ['video_0102.mov']
        }

        response = self.test_client.post(
            '/api/v1/incidents',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token},
            content_type='application/json',
            data=json.dumps(red_flag)
        )

        message = json.loads(response.data)
        self.assertEqual(message['status'], 201)

    def test_add_bad_red_flag(self):
        """
        Test adding a red flag without a title
        Expect 400
        """
        red_flag = {
            'comment': 'Took a bribe',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'status': 'pending',
            'images': ['photo_0979.jpg'],
            'videos': ['mov_0987.mp4']
        }

        response = self.test_client.post(
            '/api/v1/incidents',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token},
            content_type='application/json',
            data=json.dumps(red_flag)
            )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 400)

    def test_get_all_red_flags_as_admin(self):
        """
        Test getting all red flags as a normal user
        token is by an administrative user
        2 red flag expected
        """
        response = self.test_client.get(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' + self.admin_token})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)

    def test_get_all_redflags_as_non_admin(self):
        """
        Test getting all red flags when user is not admin
        """
        response = self.test_client.get(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
   
    def test_get_non_existent_red_flag(self):
        """
        Test getting one red flag that does not exist
        Expect 404
        """
        response = self.test_client.get(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)
