import json
from api import app, test_client


class TestBase():
    """
    Class containing common test procedures
    """
    def create_user_data(self, **kwags):
        return {
            'user_name': kwags.get('user_name', 'bison'),
            'email': kwags.get('email', 'bisonlou@ireporter.com'),
            'first_name': kwags.get('first_name', 'bison'),
            'last_name':  kwags.get('last_name', 'lou'),
            'phone_number':  kwags.get('phone_number', '0753669897'),
            'password': kwags.get('password', 'Pa$$word123'),
            'other_names':  kwags.get('other_names',''),
            'is_admin':  kwags.get('is_admin', False)
        }

    def create_incident_data(self, **kwags):
        return {
            'title': kwags.get('title', 'title'),
            'comment': kwags.get('comment', 'title'),
            'latitude': kwags.get('latitude', 0.0001),
            'longitude': kwags.get('longitude', 0.0001),
            'type':  kwags.get('type', 'red-flag'),
            'status':  kwags.get('status', 'pending'),
            'images': kwags.get('images', ['photo_0.jpg']),
            'videos':  kwags.get('videos', ['video_0002.mov'])
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

    def get_user(self, token):
        return test_client.get(
                '/api/v1/auth/user',
                headers={'Authorization': 'Bearer ' + token})

    def post_n_get_token(self, credentials):
        token = self.get_token(credentials)
        self.post_incident(credentials)

        return token

    def post_incident(self, credentials, data = dict()):
        incident = self.create_incident_data(**data)
        token = self.get_token(credentials)

        return test_client.post(
            '/api/v1/incidents',
            content_type='application/json',
             headers={'Authorization': 'Bearer ' + token},
            data=json.dumps(incident))

    def get_incidents(self, credentials, types):
        token = self.post_n_get_token(credentials)

        return test_client.get(
            '/api/v1/'+ types,
            headers={'Authorization': 'Bearer ' + token})

    def get_totals(self, credentials):
        token = self.post_n_get_token(credentials)

        return test_client.get(
            '/api/v1/incidents/totals',
            headers={'Authorization': 'Bearer ' + token})

    def get_incident(self, credentials, incident_id):
        token  = self.post_n_get_token(credentials)

        return test_client.get(
            '/api/v1/incidents/'+ incident_id,
            headers={'Authorization': 'Bearer ' + token})

    def patch_incident(self, credentials, incident_id, key):
        token = self.post_n_get_token(credentials)
        data = self.create_incident_data()

        return test_client.patch(
            '/api/v1/incidents/'+ incident_id + '/' + key,
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + token},
            data=json.dumps(data))

    def put_incident(self, credentials, incident_id):
        token = self.post_n_get_token(credentials)
        data = self.create_incident_data()

        return test_client.put(
            '/api/v1/incidents/'+ incident_id,
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + token},
            data=json.dumps(data))

    def delete_incident(self, credentials, incident_id):
        token = self.post_n_get_token(credentials)

        return test_client.delete(
            '/api/v1/incidents/'+ incident_id,
            headers={'Authorization': 'Bearer ' + token})

    def get_welcome(self):
        return test_client.get(
            '/')

    