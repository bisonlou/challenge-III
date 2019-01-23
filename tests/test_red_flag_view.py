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
            'other_names': ''
        }

        user_2 = {
            'user_name': 'bison',
            'email': 'bisonlou@yahoo.com',
            'date_registered': '2019-01-01',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': ''
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

        self.admin_token = json.loads(response_1.data)
        self.non_admin_token = json.loads(response_2.data)

        red_flag_1 = {
            'created_on': '2018-12-24',
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234},
                       {'id': 2, 'name': 'photo_0094.jpg', 'size': 200}],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}]
        }

        red_flag_2 = {
            'created_on': '2018-12-12',
            'title': 'Magistrate',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}]
        }

        self.test_client.post(
            '/api/v1/incidents',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['data'][0]['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag_1)
        )

        self.test_client.post(
            '/api/v1/incidents',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['data'][0]['access_token']},
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
            'created_on': '2018-12-24',
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'images': [{'id': 1, 'name': 'photo_0912.jpg', 'size': 134}],
            'videos': [{'id': 1, 'name': 'video_0102.mov', 'size': 2220}]
        }

        response = self.test_client.post(
            '/api/v1/incidents',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['data'][0]['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        print(self.admin_token['data'][0]['access_token'])
        message = json.loads(response.data)
        self.assertEqual(message['status'], 201)

    def test_add_bad_red_flag(self):
        """
        Test adding a red flag with images
        and videos keys not of type list but string
        Expect 400
        """
        red_flag = {
            'created_on': '2018-12-12',
            'title': 'Police officer at CPS Badge #162',
            'comment': 'Took a bribe',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'images': 'photo_0979.jpg',
            'videos': 'mov_0987.mp4'
        }

        response = self.test_client.post(
            '/api/v1/incidents',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['data'][0]['access_token']},
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
            '/api/v1/incidents/red-flag',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['data'][0]['access_token']})
        message = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

    # def test_get_existing_red_flag(self):
    #     """
    #     Test getting one red flag that exists
    #     Expect 200
    #     """
    #     response = self.test_client.get(
    #         '/api/v1/redflags/1',
    #         headers={'Authorization': 'Bearer ' +
    #                  self.admin_token['data'][0]['access_token']})
    #     message = json.loads(response.data)

    #     self.assertEqual(message['status'], 200)

    # def test_get_red_flag_when_not_owner(self):
    #     """
    #     Test getting one red flag that does not belong to the user
    #     Expect 403
    #     """
    #     response = self.test_client.get(
    #         '/api/v1/redflags/1',
    #         headers={'Authorization': 'Bearer ' +
    #                  self.admin_token['data'][0]['access_token']})
    #     message = json.loads(response.data)

    #     self.assertEqual(message['status'], 403)

    # def test_get_non_existent_red_flag(self):
    #     """
    #     Test getting one red flag that does not exist
    #     Expect 404
    #     """
    #     response = self.test_client.get(
    #         '/api/v1/redflags/3',
    #         headers={'Authorization': 'Bearer ' +
    #                  self.admin_token['data'][0]['access_token']})
    #     message = json.loads(response.data)

    #     self.assertEqual(message['status'], 404)


    
