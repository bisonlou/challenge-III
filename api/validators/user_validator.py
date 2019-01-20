import re
from validate_email import validate_email
from api.models.user_model import User


class UserValidator():

    def has_required_fields(self, data):
        '''
        Function to check if user keys and key data is present
        Also checks if data is in required format
        Returns True on succes otherwise False

        '''
        if self.has_missing_keys(data):
            return False            

        if self.has_empty_keys(data):
            return False

        if not self.has_proper_email(data['email']):
            return False

        return True
    
    def duplicate_email(self, email):
        user_count = User.query.filter_by(email=email).count()
        if user_count > 0:
            return True
        return False
        
    def get_password_errors(self, data):
        '''
        Function to check if the given password meets minimum requrements
        Returns a dictionary of errors

        '''
        password = data['password']
        errors = {}
        if len(password) < 6 or len(password) > 12:
            errors['length'] = 'Password should be between 6 and 12 characters'
        if not re.search("[a-z]", password):
            errors['lower-char'] = 'Password should contain atleast 1 lower case character'
        if not re.search("[0-9]", password):
            errors['numerical-char'] = 'Password should contain atleast 1 number'
        if not re.search("[A-Z]", password):
            errors['upper-char'] = 'Password should contain atleast 1 upper case character'
        if not re.search("[$#@]", password):
            errors['symbol-char'] = "Password should contain atleast 1 of '$','#','@'"

        return errors

    def has_missing_keys(self, data):
        keys = ['user_name', 'password', 'first_name',
                'last_name', 'email', 'phone_number',
                'other_names']

        # get list of missing keys
        missing_keys = [key for key in keys if key not in data]
        if len(missing_keys) > 0:
            return True        
        return False
        
    def has_empty_keys(self, data):
        keys = ['user_name', 'first_name', 'last_name',
                'email', 'phone_number']

        # get list of keys with missing data
        missing_data = [key for key in keys if len(data[key]) == 0]
        if len(missing_data):
            return True
        return False

    def has_proper_email(self, email):
        return validate_email(email)
    

    
