import re
from validate_email import validate_email
from api.models.user_model import User, UserServices

user_services = UserServices()


class UserValidator():

    def has_required_fields(self, data):
        '''
        Function to check if user keys and key data is present
        Also checks if data is in required format
        Returns True on succes otherwise False

        '''
        keys = ['user_name', 'password', 'first_name',
                'last_name', 'email', 'phone_number',
                'other_names']
        if self.has_missing_keys(data, keys):
            return False

        keys = ['user_name', 'first_name', 'last_name',
                'email', 'phone_number', 'other_names']
        if self.has_unexpected_data_type(data, keys):
            return False

        keys = ['user_name', 'first_name', 'last_name',
                'email', 'phone_number']
        if self.has_empty_feilds(data, keys):
            return False

        if not self.has_proper_email(data['email']):
            return False

        return True

    def has_login_required_fields(self, data):
        '''
        Function to check if the login data is present
        Returns True on success otherwise False

        '''
        keys = ['email', 'password']

        if self.has_missing_keys(data, keys):
            return False

        if self.has_unexpected_data_type(data, keys):
            return False

        if self.has_empty_feilds(data, keys):
            return False

        return True

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

    def duplicate_email(self, email):
        user = user_services.get_user_by_email(email)
        if user:
            return True
        return False

    def has_missing_keys(self, data, keys):
        # get list of missing keys
        missing_keys = [key for key in keys if key not in data]
        if len(missing_keys) > 0:
            return True
        return False

    def has_unexpected_data_type(self, data, keys):
        improper_type = [key for key in keys if type(data[key]) is not str]
        if len(improper_type):
            return True

    def has_empty_feilds(self, data, keys):
        # get list of keys with missing data
        missing_data = [key for key in keys if len(data[key]) == 0]
        if len(missing_data):
            return True

        return False

    def has_proper_email(self, email):
        return validate_email(email)

    def has_login_required_fields(self, data):
        '''
        Function to check if the login data is present
        Returns True on success otherwise False

        '''
        keys = ['email', 'password']

        missing_data = [key for key in keys 
                        if key not in data or len(data[key]) == 0]
        if len(missing_data): 
            return False

        return True
    

