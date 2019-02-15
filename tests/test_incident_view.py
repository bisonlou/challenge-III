import unittest
from tests.test_base import TestBase
from api.database.engine import DbConnection

base = TestBase()


class TestRedFlagView(unittest.TestCase):

    def setUp(self):
        """
        Setup test client
        """
        self.db_services = DbConnection()
        self.credentials = {'email': 'bisonlou@ireporter.com',
                                    'password': 'Pa$$word123'}
        self.admin_creds = {'email': 'bisonlou@gmail.com',
                                    'password': 'Pa$$word123'}
       
    def tearDown(self):
        """
        teardown database
        """
        self.db_services.reset_database()

    def test_add_proper_red_flag(self):
        """
        Test adding a red flag with expected keys
        Expect 201
        """
        response = base.post_incident(self.credentials)
        self.assertEqual(response.status_code, 201)

    def test_add_proper_red_flag_as_admin(self):
        """
        Test adding a red flag with expected keys as admin
        Expect 403
        """
        response = base.post_incident(self.admin_creds)
        self.assertEqual(response.status_code, 403)

    def test_add_bad_red_flag(self):
        """
        Test adding a red flag without empty title
        Expect 400
        """        
        data = {'title': ''}
        response = base.post_incident(self.credentials, data)
        self.assertEqual(response.status_code, 400)

    def test_get_all_interventions(self):
        """
        Test getting all red flags as a normal user
        token is by an administrative user
        2 red flag expected
        """
        response = base.get_incidents(self.credentials, 'interventions')
        self.assertEqual(response.status_code, 200)

    def test_get_all_redflags(self):
        """
        Test getting all red flags when user is not admin
        """
        response = base.get_incidents(self.credentials, 'redflags')
        self.assertEqual(response.status_code, 200)

    def test_get_red_flag(self):
        """
        Test getting one red flags
        Expect 200
        """
        response = base.get_incident(self.credentials, '1')
        self.assertEqual(response.status_code, 200)

    def test_get_intervention(self):
        """
        Test getting one intervention that does not exist
        Expect 200
        """
        response = base.get_incident(self.credentials, '1')
        self.assertEqual(response.status_code, 200)

    def test_get_non_existent_red_flag(self):
        """
        Test getting one red flag that does not exist
        Expect 404
        """
        response = base.get_incident(self.credentials, '2')
        self.assertEqual(response.status_code, 404)

    def test_patch_incident_comment(self):
        """
        Test patching an incidents comment
        Expect 200
        """        
        response = base.patch_incident(self.credentials, '1', 'comment')
        self.assertEqual(response.status_code, 200)

    def test_patch_incident_location(self):
        """
        Test patching an incidents comment
        Expect 200
        """        
        response = base.patch_incident(self.credentials, '1', 'location')
        self.assertEqual(response.status_code, 200)

    def test_patch_incident_location_as_admin(self):
        """
        Test patching an incidents comment as admin
        Expect 403
        """        
        response = base.patch_incident(self.admin_creds, '1', 'location')
        self.assertEqual(response.status_code, 403)

    def test_patch_non_existentincident_location(self):
        """
        Test patching an incidents location that doesnt exist
        Expect 200
        """        
        response = base.patch_incident(self.credentials, '2', 'location')
        self.assertEqual(response.status_code, 404)

    def test_patch_incident_status_as_non_admin(self):
        """
        Test patching an incidents status
        Expect 403
        """
        response = base.patch_incident(self.credentials, '1', 'status')
        self.assertEqual(response.status_code, 403)

    def test_patch_incident_status_as_admin(self):
        """
        Test patching an incidents status as admin
        Expect 404
        """
        response = base.patch_incident(self.admin_creds, '1', 'status')
        self.assertEqual(response.status_code, 404)

    def test_patch_non_existent_incident(self):
        """
        Test patching an incident that doesn't exist
        Expect 200
        """
        response = base.patch_incident(self.credentials, '2', 'comment')
        self.assertEqual(response.status_code, 404)

    def test_put_incident(self):
        """
        Test putting an incidents location
        Expect 200
        """
        response = base.put_incident(self.credentials, '1')
        self.assertEqual(response.status_code, 200)

    def test_put_non_existent_incident(self):
        """
        Test putting an incident that doesnt exist
        Expect 200
        """
        response = base.put_incident(self.credentials, '2')
        self.assertEqual(response.status_code, 404)

    def test_put_incident_as_admin(self):
        """
        Test putting an incident as admin
        Expect 403
        """
        response = base.put_incident(self.admin_creds, '1')
        self.assertEqual(response.status_code, 403)

    def test_delete_incident(self):
        """
        Test deleting an incidents location
        Expect 200
        """
        response = base.delete_incident(self.credentials, '1')
        self.assertEqual(response.status_code, 200)

    def test_delete_incident_as_admin(self):
        """
        Test deleting an incidents location as admin
        Expect 403
        """

        response = base.delete_incident(self.admin_creds, '1')
        self.assertEqual(response.status_code, 403)

    def test_welcome(self):
        """
        Test deleting an incidents that doesnt exist
        Expect 200
        """
        response = base.get_welcome()
        self.assertEqual(response.status_code, 200)
