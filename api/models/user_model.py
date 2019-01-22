import psycopg2
import psycopg2.extras

class User():

    def __init__(self, **kwags):
        self._id = kwags.get('id', 0)
        self._user_name = kwags.get('user_name','')
        self._email = kwags.get('email', '')
        self._password = kwags.get('password','')
        self._phone_number = kwags.get('phone_number','')
        self._date_registered = kwags.get('date_registered','')
        self._first_name = kwags.get('first_name', '')
        self._last_name = kwags.get('last_name','')
        self._other_names = kwags.get('other_names','')
        self._is_admin = kwags.get('is_admin','')

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def is_admin(self):
        return self._is_admin
         
    @property
    def user_name(self):
        return self._user_name

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def other_names(self):
        return self._other_names

    @property
    def phone_number(self):
        return self._phone_number

    @property
    def date_registered(self):
        return self._date_registered    


class UserServices():

    def __init__(self):

        self.db_name = 'ireporter'

        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name, user='postgres', host='localhost', password=''
            )
            # self.connection = psycopg2.connect(
            #     dbname=self.db_name, user='postgres', host='localhost', password='system#2008', port=5432
            # )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            create_users_table = "CREATE TABLE IF NOT EXISTS users \
                                 (id SERIAL NOT NULL PRIMARY KEY, \
                                 userName TEXT NOT NULL,\
                                 email TEXT NOT NULL,\
                                 password TEXT NOT NULL,\
                                 firstName TEXT NOT NULL,\
                                 lastName TEXT NOT NULL,\
                                 otherNames TEXT NOT NULL,\
                                 phoneNumber TEXT NOT NULL,\
                                 dteRegistered TEXT NOT NULL,\
                                 isAdmin Boolean NOT NULL\
                                 );"

            self.cursor.execute(create_users_table)

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
            select_query = "SELECT * FROM users WHERE users.id = {};".format(value)
        elif key == 'email':
            select_query = "SELECT * FROM users WHERE users.email = '{}';".format(value)

        self.cursor.execute(select_query)
        user = self.cursor.fetchone()
        # only return if ther is a user found
        if not user is None:
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

    def remove_all(self):
        delete_query = 'DELETE FROM users;'
        self.cursor.execute(delete_query)
        
