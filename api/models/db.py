import psycopg2
import psycopg2.extras


class DbConnection():

    def __init__(self):
        self.db_name = 'ireporter'

        try:
            # self.connection = psycopg2.connect(
            #     dbname=self.db_name, user='postgres', host='localhost',
            #     password='system#2008', port=5432
            # )
            self.connection = psycopg2.connect(
                dbname=self.db_name, user='postgres', host='localhost',
                password='')

            self.connection.autocommit = True
            self.cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

            create_tables = '''
                            CREATE TABLE IF NOT EXISTS public.users (id SERIAL NOT NULL PRIMARY KEY, userName TEXT NOT NULL,
                                email TEXT NOT NULL, password TEXT NOT NULL, firstName TEXT NOT NULL, lastName TEXT NOT NULL,
                                otherNames TEXT NOT NULL, phoneNumber TEXT NOT NULL, dteRegistered TEXT NOT NULL,
                                isAdmin Boolean NOT NULL);
                            CREATE TABLE IF NOT EXISTS incidents(id SERIAL NOT NULL PRIMARY KEY, createdOn TIMESTAMP,
                                title TEXT NOT NULL, comment TEXT NOT NULL,
                                type varchar(25), createdBy INTEGER, location VARCHAR(50) NOT NULL,
                                status varchar(20) NOT NULL, FOREIGN KEY (createdBy) REFERENCES users (id)
                                ON UPDATE CASCADE ON DELETE CASCADE);
                            CREATE TABLE IF NOT EXISTS public.images(id SERIAL NOT NULL PRIMARY KEY, 
                                incident INTEGER, filename CHARACTER VARCHAR(255) NOT NULL,
                                FOREIGN KEY (incident) REFERENCES incidents(id) ON UPDATE CASCADE ON DELETE CASCADE);
                            CREATE TABLE IF NOT EXISTS videos( id INTEGER, incident INTEGER, filename VARCHAR(255) NOT NULL,
                                FOREIGN KEY (incident) REFERENCES incidents (id) ON UPDATE CASCADE ON DELETE CASCADE 
                            ); 
                        '''
            self.cursor.execute(create_tables)
        except:
            print('Failed to connect to the database.')

    def add_user(self, user):
        new_user = "INSERT INTO users \
                    (username, email, password, firstName,\
                    lastName, otherNames, phoneNumber, dteRegistered, isAdmin)\
                    VALUES('{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}');".format(
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
        # only return if ther is a user found
        if is not user:
            return user

    # def get_all(self):
    #     return [user.to_dict() for user in user_table]

    # # def delete_user(self, user_id):
    # #     users = self.get_user(user_id)
    # #     if len(users) > 0:
    # #         user_table.remove(users[0])

    # # def promote_user(self, user_id):
    # #     users = self.get_user_by_id(user_id)
    # #     if len(users) > 0:
    # #         users[0].is_admin = True

    # def count(self):
    #     return len(user_table)

    def delete_all_users(self):
        delete_query = 'DELETE FROM users;'
        self.cursor.execute(delete_query)

    def insert_incident(self, incident):
        new_incident = "INSERT INTO incidents \
                    (createdOn, title, comment, type,\
                     createdBy, location, status) \
                    VALUES('{}', '{}', '{}','{}', '{}', '{}','{}');".format(
            incident.created_on, incident.title, incident.comment,
            incident.incident_type, incident.created_by, incident.location,
            incident.status)

        self.cursor.execute(new_incident)

    def count(self, incident_type):
        if incident_type == 'red-flag':
            return len(redflag_table)
        elif incident_type == 'intervention':
            return len(intervention_table)

    def get_all(self, user_id, is_admin, incident_type):
        # check  incident type
        table = []
        if incident_type == 'red-flag':
            table = redflag_table
        if incident_type == 'intervention':
            table = intervention_table

        # check if user is admin
        if is_admin is True:
            return [incident.to_dict() for incident in table]
        else:
            return [incident.to_dict() for incident in table
                    if incident.created_by == user_id]

    def delete_all_incidents(self):
        delete_query = 'DELETE FROM incidents;'
        self.cursor.execute(delete_query)

    def get_incident(self, incident_id, incident_type):
        # covert flag item to dictionaties
        incidents = []
        if incident_type == 'red-flag':
            incidents = [incident for incident in
                         redflag_table if incident.id == incident_id]
        elif incident_type == 'intervention':
            incidents = [incident for incident in
                         intervention_table if incident.id == incident_id]

        if len(incidents) > 0:
            return incidents[0]

    def put_incident(self, existing_incident, update_incident, incident_type):
        keys = ['title', 'location', 'images', 'videos', 'created_on',
                'comment', 'status']
        for key in keys:
            self.patch_incident(existing_incident, update_incident, key)

    def patch_incident(self, existing_incident, update_incident, key):
        setattr(existing_incident, key, getattr(update_incident, key))

    def delete_incident(self, incident, incident_type):
        if incident_type == 'red-flag':
            redflag_table.remove(incident)
        elif incident_type == 'intervention':
            intervention_table.remove(incident)

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
