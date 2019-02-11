import psycopg2
import psycopg2.extras
from os import environ
from api.models.incident_model import Incident


class DbConnection():

    def __init__(self):

        try:
            self.connection = psycopg2.connect(environ.get('URI'))
            self.connection.autocommit = True

            self.cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

            self.cursor.execute(open('api/database/create_db.sql', 'r').read())

        except Exception as e:
            print(e)
            print('Failed to connect to the database.')

    def add_user(self, user):
        new_user = self.insert_query_builder(
            ['username', 'email', 'password', 'firstname', 'lastname',
             'othernames', 'phonenumber', 'dteregistered', 'isadmin'],
            'users')
        data = (user.user_name, user.email, user.password,
                user.first_name, user.last_name, user.other_names,
                user.phone_number, user.date_registered, user.is_admin)

        self.cursor.execute(new_user, data)
        inserted_user = self.get_user_by_email(user.email)

        return inserted_user

    def get_user_by_id(self, user_id):
        return self.get_user('id', user_id)

    def get_user_by_email(self, login_email):
        return self.get_user('email', login_email)

    def get_user(self, key, value):
        select_query = self.select_query_builder(
                         ['*'],
                         'users', [key])

        data = (value,)
        self.cursor.execute(select_query, data)
        user = self.cursor.fetchone()

        if user:
            return user

    def get_users(self):
        select_query = self.select_query_builder(
                         ['username', 'email', 'firstname', 'lastname',
                          'othernames', 'phonenumber', 'dteregistered', 'isadmin'],
                         'users', [])

        self.cursor.execute(select_query)
        users = self.cursor.fetchall()

        if users:
            return users

    def insert_incident(self, incident):
        fields = ['createdOn', 'title', 'comment', 'type',
                  'createdby', 'latitude', 'longitude', 'status']
        values = (incident.createdon, incident.title, incident.comment,
                  incident.type, incident.createdby, incident.latitude,
                  incident.longitude, incident.status)

        new_incident = self.insert_query_builder(fields, 'incidents')
        self.cursor.execute(new_incident, values)

        result = self.cursor.fetchone()
        incident_id = result['id']

        self.insert_incident_media(incident_id, incident.images, 'images')
        self.insert_incident_media(incident_id, incident.videos, 'videos')

        return incident_id

    def get_all_incidents(self, user_id, incident_type):
        # check if user is admin
        if self.check_user_is_admin(user_id):
            incidents_query = self.select_query_builder(
                ['*'], 'incidents', ['type'])
            data = (incident_type,)

            self.cursor.execute(incidents_query, data)
            incidents = self.cursor.fetchall()
            return incidents

        else:
            incidents_query = self.select_query_builder(
                ['*'], 'incidents',
                ['type', 'createdby'])
            incident_values = (incident_type, user_id)
            self.cursor.execute(incidents_query, incident_values)
            incidents = self.cursor.fetchall()

        return incidents

    def get_user_totals(self, user_id, incident_type):
        total_incident_count = self.select_query_builder(
            ['Count(id)'], 'incidents',
            ['type', 'createdby'])
        incident_values = (incident_type, user_id)
        self.cursor.execute(total_incident_count, incident_values)
        total_incidents = self.cursor.fetchone()

        rejected_incident_count = self.select_query_builder(
            ['Count(id)'], 'incidents',
            ['type', 'status', 'createdby'])
        total_rejected_values = (incident_type, 'rejected', user_id)
        self.cursor.execute(rejected_incident_count, total_rejected_values)
        total_rejected = self.cursor.fetchone()

        pending_incident_count = self.select_query_builder(
            ['Count(id)'], 'incidents',
            ['type', 'status', 'createdby'])
        total_pending_values = (incident_type, 'pending', user_id)
        self.cursor.execute(pending_incident_count, total_pending_values)
        total_pending = self.cursor.fetchone()

        return {'total': total_incidents,
                'pending': total_pending,
                'rejected': total_rejected}

    def get_incident(self, incident_id):
        '''
        Function to get just one incident
        Requires a user id to check for user rights
        Returns a user dictionary
        '''
        incidents_query = self.select_query_builder('*', 'incidents', ['id'])
        data = (incident_id,)

        self.cursor.execute(incidents_query, data)
        incident = self.cursor.fetchone()
        if incident:
            incident_obj = Incident(**incident)

            images = self.get_incident_media(incident_id, 'images')
            if images:
                for image in images:
                    incident_obj.add_image(image['filename'])

            videos = self.get_incident_media(incident_id, 'videos')
            if videos:
                for video in videos:
                    incident_obj.add_video(video['filename'])

            return incident_obj

    def put_incident(self, update_incident):
        '''Function to update an incident'''

        update_query = self.update_query_builder(
                        ['title', 'latitude', 'longitude', 'comment'],
                        'incidents',
                        ['id'])
        values = (update_incident.title,
                  update_incident.latitude,
                  update_incident.longitude,
                  update_incident.comment,
                  update_incident.id)

        self.cursor.execute(update_query, values)
        returned_data = self.cursor.fetchone()

        if returned_data:
            incident_id = returned_data['id']

            updated_incident = self.get_incident(incident_id)
            return updated_incident

    def patch_incident(self, update_incident, update_field):
        """
        Updates an incident field
        Returns the updated incident"
        """
        update_query = ""
        values = ""

        if update_field == 'location':
            update_query = self.update_query_builder(
                        ['latitude', 'longitude'], 'incidents', ['id'])
            values = (update_incident.latitude, update_incident.longitude,
                      update_incident.id)
        else:
            update_query = self.update_query_builder(
                            [update_field], 'incidents', ['id'])
            values = (getattr(update_incident, update_field), update_incident.id)

        self.cursor.execute(update_query, values)
        returned_data = self.cursor.fetchone()

        if returned_data:
            incident_id = returned_data['id']
            updated_incident = self.get_incident(incident_id)

            return updated_incident

    def add_incident_image(self, incident_id, filename):
        '''
        Function to add an image to an incident
        First deletes existing images
        Requires an incident id and the file name
        Returns a the image record id
        '''
        delete_query = self.delete_query_builder('images', ['incident'])
        self.cursor.execute(delete_query, (incident_id, ))

        query = self.insert_query_builder(['incident', 'filename'], 'images')
        self.cursor.execute(query, (incident_id, filename))

        return self.cursor.fetchone()['id']

    def delete_incident(self, incident_id):
        '''
        Function to delete one incident
        Requires a an incident id
        Returns the deleted incidents id
        '''
        delete_incidents_query = self.delete_query_builder(
                                'incidents',
                                ['id'])

        self.cursor.execute(delete_incidents_query, (incident_id,))
        returned_data = self.cursor.fetchone()

        if returned_data:
            deleted_id = returned_data['id']

            return deleted_id

    def check_user_is_admin(self, user_id):
        query = self.select_query_builder(
            ['isadmin'], 'users',
            ['id'])
        self.cursor.execute(query, (user_id,))
        query_result = self.cursor.fetchone()

        if query_result:
            return query_result['isadmin']

    def get_incident_media(self, incident_id, table):
        '''
        Function to fetch an incident media
        '''
        query = self.select_query_builder('*', table, ['incident'])
        data = (incident_id,)

        self.cursor.execute(query, data)
        media = self.cursor.fetchall()
        if media:
            return media

    def reset_database(self):
        self.cursor.execute(open('api/database/reset_db.sql', 'r').read())

    def insert_incident_media(self, incident_id, media_list, table):
        for media in media_list:
            fields = ['incident', 'filename']
            values = (incident_id, media)

            query = self.insert_query_builder(fields, table)
            self.cursor.execute(query, values)

    def select_query_builder(self, fields, table, constraints):
        ''' Function to concatenate select qurey strings and parameters'''
        query = 'SELECT '

        j = 1
        for field in fields:
            if j < len(fields):
                query = query + field + ', '
                j += 1
            else:
                query = query + field
        query = query + ' FROM ' + table

        if len(constraints) > 0:
            query = query + ' WHERE '            
            query = self.append_where_clauses(query, constraints, False)     

        return query

    def insert_query_builder(self, fields, table):
        ''' Function to concatenate insert qurey strings and parameters'''
        query = 'INSERT  INTO ' + table + ' ('

        j = 1
        for field in fields:
            if j < len(fields):
                query = query + field + ', '
                j += 1
            else:
                query = query + field
        query = query + ') VALUES ('

        for i in range(len(fields)):
            if i + 1 < len(fields):
                query = query + '%s, '
            else:
                query = query + '%s) RETURNING id;'
        return query

    def update_query_builder(self, fields, table, constraints):
        ''' Function to concatenate update qurey strings and parameters'''
        query = 'UPDATE ' + table + ' SET '

        j = 1
        for field in fields:
            if j < len(fields):
                query = query + field + ' = %s, '
                j += 1
            else:
                query = query + field + ' = %s'

        query = query + ' WHERE '
        query = self.append_where_clauses(query, constraints, True)

        return query

    def delete_query_builder(self, table, constraints):
        ''' Function to concatenate delete qurey strings and parameters'''
        query = 'DELETE FROM ' + table + ' WHERE '
        query = self.append_where_clauses(query, constraints, True)

        return query

    def append_where_clauses(self, query, constraints, return_id):
        i = 1
        for constraint in constraints:
            if i < len(constraints):
                query = query + constraint + ' = %s AND '
                i += 1
            else:
                if return_id:
                    query = query + constraint + ' = %s  RETURNING id;'
                else:
                    query = query + constraint + ' = %s;'        
        return query
