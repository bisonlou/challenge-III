from os import environ
import psycopg2
import psycopg2.extras


class DbConnection():

    def __init__(self):
        self.db_name = 'ireporter'

        try:
            self.connection = psycopg2.connect(environ.get('URI'))
            
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

            create_tables = '''
                            CREATE TABLE IF NOT EXISTS public.users (id SERIAL
                             NOT NULL PRIMARY KEY, userName TEXT NOT NULL,
                                email TEXT NOT NULL, password TEXT NOT NULL,
                                 firstName TEXT NOT NULL,
                                 lastName TEXT NOT NULL,
                                otherNames TEXT NOT NULL, phoneNumber TEXT NOT
                                 NULL, dteRegistered TEXT NOT NULL,
                                isAdmin Boolean NOT NULL);
                            CREATE TABLE IF NOT EXISTS incidents(id SERIAL NOT
                                 NULL PRIMARY KEY, createdOn TIMESTAMP,
                                title TEXT NOT NULL, comment TEXT NOT NULL,
                                type varchar(25), createdBy INTEGER, location
                                 VARCHAR(50) NOT NULL,
                                status varchar(20) NOT NULL, FOREIGN KEY
                                 (createdBy) REFERENCES users (id)
                                ON UPDATE CASCADE ON DELETE CASCADE);
                            CREATE TABLE IF NOT EXISTS public.images(id SERIAL
                             NOT NULL PRIMARY KEY,
                                incident INTEGER NOT NULL, filename
                                 VARCHAR(255) NOT NULL,
                                FOREIGN KEY (incident) REFERENCES incidents(id)
                                 ON UPDATE CASCADE ON DELETE CASCADE);
                            CREATE TABLE IF NOT EXISTS videos( id SERIAL
                             NOT NULL PRIMARY KEY, incident INTEGER NOT NULL,
                              filename VARCHAR(255) NOT NULL,
                                FOREIGN KEY (incident) REFERENCES incidents
                                 (id) ON UPDATE CASCADE ON DELETE CASCADE
                            );
                        '''
            self.cursor.execute(create_tables)
        except Exception as e:
            print(e)
            print('Failed to connect to the database.')

    def add_user(self, user):
        new_user = "INSERT INTO users \
                    (username, email, password, firstName, lastName,\
                     otherNames, phoneNumber, dteRegistered, isAdmin)\
                    VALUES('{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}')\
                    ;".format(
            user.user_name, user.email, user.password, user.first_name,
            user.last_name, user.other_names, user.phone_number,
            user.date_registered, user.is_admin)

        self.cursor.execute(new_user)
        inserted_user = self.get_user_by_email(user.email)

        return inserted_user

    def get_user_by_id(self, user_id):
        return self.get_user('id', user_id)

    def get_user_by_email(self, login_email):
        return self.get_user('email', login_email)

    def get_user(self, key, value):
        if key == 'id':
            select_query = "SELECT * FROM users WHERE users.id = {};".format(
                value)
        elif key == 'email':
            select_query = "SELECT * FROM users \
                            WHERE users.email = '{}';".format(value)

        self.cursor.execute(select_query)
        user = self.cursor.fetchone()

        if user:
            return user

    def delete_all_users(self):
        delete_query = 'DELETE FROM users;'
        self.cursor.execute(delete_query)

    def insert_incident(self, incident):
        new_incident = "INSERT INTO incidents \
                    (createdOn, title, comment, type,\
                     createdBy, location, status) \
                    VALUES('{}', '{}', '{}','{}', '{}', '{}','{}')\
                    RETURNING id;".format(
            incident.created_on, incident.title, incident.comment,
            incident.incident_type, incident.created_by, incident.location,
            incident.status)

        self.cursor.execute(new_incident)
        result = self.cursor.fetchone()
        incident_id = result['id']

        images = incident.images
        for image in images:
            new_incident_image = "INSERT INTO images \
                            (incident, filename) values \
                            ({}, '{}');".format(incident_id, image)

            self.cursor.execute(new_incident_image)

        videos = incident.videos
        for video in videos:
            new_incident_video = "INSERT INTO videos \
                            (incident, filename) values \
                            ({}, '{}');".format(incident_id, video)

            self.cursor.execute(new_incident_video)

        return incident_id

    def get_all_incidents(self, user_id, incident_type):
        query = ""
        # check if user is admin
        if self.check_user_is_admin(user_id):
            incidents_query = "select * from incidents inner join images \
                             ON incidents.id = images.incident \
                             INNER JOIN videos \
                             ON incidents.id = videos.incident \
                             WHERE incidents.type = '{}';\
                            ".format(incident_type)
        else:
            incidents_query = "select * from incidents inner join images \
                             on incidents.id = images.incident \
                             INNER JOIN videos \
                             ON incidents.id = videos.incident \
                             WHERE incidents.type = '{}' \
                             AND incidents.createdby = {};".format(
                incident_type, user_id)

        self.cursor.execute(incidents_query)
        returned_incidents = self.cursor.fetchall()

        return returned_incidents

    def delete_all_incidents(self):
        delete_query = 'DELETE FROM incidents;'
        self.cursor.execute(delete_query)

    def get_incident(self, user_id, incident_id):
        '''
        Function to get just one incident
        Requires a user id to check user type
        Returns a uder dictionary
        '''
        incidents_query = ""

        if self.check_user_is_admin(user_id):
            incidents_query = "select * from incidents \
                             WHERE incidents.id = {};\
                            ".format(incident_id)
        else:
            incidents_query = "select * from incidents \
                            WHERE incidents.id = {} \
                            AND incidents.createdby = {};".format(
                incident_id, user_id)

        self.cursor.execute(incidents_query)
        incident = self.cursor.fetchone()

        return incident

    def put_incident(self, update_incident):
        update_query = "UPDATE incidents SET title = '{}', location = '{}', comment = '{}'  WHERE id = {} AND createdby = {} RETURNING id".format(
            update_incident.title,
            update_incident.location,
            update_incident.comment,
            update_incident.id,
            update_incident.created_by)

        self.cursor.execute(update_query)
        returned_data = self.cursor.fetchone()

        incident_id = returned_data['id']
        updated_incident = self.get_incident(update_incident.created_by,
                                             incident_id)

        return updated_incident

    def patch_incident(self, update_incident, update_key):
        update_query = "UPDATE incidents SET {} = '{}' WHERE id = {} and createdby = {} RETURNING id".format(
            update_key,
            getattr(update_incident, update_key),
            update_incident.id,
            update_incident.created_by)

        self.cursor.execute(update_query)
        returned_data = self.cursor.fetchone()

        incident_id = returned_data['id']
        updated_incident = self.get_incident(update_incident.created_by,
                                             incident_id)

        return updated_incident

    def delete_incident(self, incident_id):
        delete_incidents_query = "DELETE FROM incidents WHERE id = {} RETURNING id".format(
                                 incident_id)

        delete_images_query = "DELETE FROM images WHERE id = {} RETURNING id".format(
            incident_id)

        delete_videos_query = "DELETE FROM videos WHERE id = {} RETURNING id".format(
            incident_id)

        self.cursor.execute(delete_images_query)
        self.cursor.execute(delete_videos_query)
        returned_data = self.cursor.fetchone()

        if returned_data:
            deleted_id = returned_data['id']

            return deleted_id

    def escalate_incident(self, incident):
        # get current status
        status = incident.status

        # increment status by 1 if status is less than 3
        if status < 3:
            status += 1

        # set new status
        incident.status = status

    def reject(self, incident):
        # set status to -1 to match last item in status list
        incident.status = -1

    def check_user_is_admin(self, user_id):
        query = "SELECT isadmin from users WHERE id = {}".format(user_id)
        self.cursor.execute(query)
        query_result = self.cursor.fetchone()

        if query_result:
            return query_result['isadmin']

    def get_incident_images(self, incident_id):
        '''
        Function to fetch an incidents images
        '''
        images_query = "select filename from images \
                            WHERE incident = {};\
                            ".format(incident_id)
        images = self.cursor.execute(images_query)
        if images:
            return images

    def get_incident_videos(self, incident_id):
        '''
        Function to fetch an incidents videos
        '''
        videos_query = "select filename from videos \
                            WHERE incident = {};\
                            ".format(incident_id)
        videos = self.cursor.execute(videos_query)
        if videos:
            return videos
