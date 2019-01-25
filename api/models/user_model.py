
class User():

    def __init__(self, **kwags):
        self._id = kwags.get('id', 0)
        self._user_name = kwags.get('user_name', '')
        self._email = kwags.get('email', '')
        self._password = kwags.get('password', '')
        self._phone_number = kwags.get('phone_number', '')
        self._date_registered = kwags.get('date_registered', '')
        self._first_name = kwags.get('first_name', '')
        self._last_name = kwags.get('last_name', '')
        self._other_names = kwags.get('other_names', '')
        self._is_admin = kwags.get('is_admin', '')

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



       

    
        
