import json
from api import app, test_client


class TestBase():
    """
    Class containing common test procedures
    """
    def create_user_data(self, **kwags):
        return {
            'user_name': kwags.get('user_name', 'bison'),
            'email': kwags.get('email', 'bisonlou@gmail.com'),
            'first_name': kwags.get('first_name', 'bison'),
            'last_name':  kwags.get('last_name', 'lou'),
            'phone_number':  kwags.get('phone_number', '0753669897'),
            'password': kwags.get('password', 'Pa$$word123'),
            'other_names':  kwags.get('other_names',''),
            'is_admin':  kwags.get('is_admin', False)
        }

    def register_user(self, data = dict()):
        user = self.create_user_data(**data)

        return test_client.post(
            '/api/v1/auth/signup',
            content_type='application/json',
            data=json.dumps(user))

    def login_user(self, credentials):
        self.register_user()

        return test_client.post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(credentials))

    def get_token(self, credentials):
        response = self.login_user(credentials)
        message = json.loads(response.data)

        return message['data'][0]['access_token']

    def get_users(self, token):
        return test_client.get(
                '/api/v1/auth/users',
                headers={'Authorization': 'Bearer ' + token})
    