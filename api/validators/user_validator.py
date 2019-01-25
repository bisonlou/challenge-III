import re
from validate_email import validate_email
from api.models.user_model import User
from api.models.db import DbConnection
from flask import jsonify

db_services = DbConnection()


class UserValidator():

    def has_required_fields(self, data):
        '''
        Function to check if user keys and key data is present
        Also checks if data is in required format
        Returns True on success otherwise False

        '''
        keys = ['user_name', 'password', 'first_name',
                'last_name', 'email', 'phone_number',
                'other_names', 'is_admin']
        missing_keys = self.has_missing_keys(data, keys)
        if len(missing_keys) > 0:
            return missing_keys

        keys = ['user_name', 'first_name', 'last_name',
                'email', 'phone_number', 'other_names']
        bad_data = self.has_unexpected_data_type(data, keys)
        if len(bad_data) > 0:
            return bad_data

        keys = ['user_name', 'first_name', 'last_name',
                'email', 'phone_number']
        empty_fields = self.has_empty_feilds(data, keys)
        if len(empty_fields) > 0:
            return empty_fields

        bad_email = self.has_proper_email(data['email'])
        if bad_email:
            return bad_email

        bad_phone_number = self.has_bad_phone_number(data['phone_number'])
        if bad_phone_number:
            return bad_phone_number

        keys = ['first_name', 'last_name', 'other_names']
        bad_name = self.has_bad_name(data, keys)
        if bad_name:
            return bad_name

        password_errors = self.has_password_errors(data['password'])
        if len(password_errors) > 0:
            return password_errors

    def has_login_required_fields(self, data):
        '''
        Function to check if the login data is present
        Returns True on success otherwise False

        '''
        keys = ['email', 'password']

        missing_keys = self.has_missing_keys(data, keys)
        if len(missing_keys) > 0:
            return missing_keys

        bad_data = self.has_unexpected_data_type(data, keys)
        if len(bad_data) > 0:
            return bad_data

        empty_fields = self.has_empty_feilds(data, keys)
        if len(empty_fields) > 0:
            return empty_fields

    def has_password_errors(self, password):
        '''
        Function to check if the given password meets minimum requrements
        Returns a dictionary of errors
        '''
        errors = []

        if len(password) < 6 or len(password) > 12:
            errors.append('Password should be between 6 and 12 characters')
        if not re.search("[a-z]", password):
            errors.append('Password should contain atleast 1 ' +
                          'lower case character')
        if not re.search("[0-9]", password):
            errors.append('Password should contain atleast 1 number')
        if not re.search("[A-Z]", password):
            errors.append('Password should contain atleast ' +
                          '1 upper case character')
        if not re.search("[$#@]", password):
            errors.append("Password should contain atleast 1 of '$','#','@'")

        return errors

    def Check_for_duplicate_email(self, email):
        user = db_services.get_user_by_email(email)
        if user:
            return True
        return False

    def has_missing_keys(self, data, keys):
        """Get missing keys in a list"""
        missing_keys = []
        for key in keys:
            if key not in data:
                missing_keys.append('{} missing'.format(key))
        return missing_keys

    def has_unexpected_data_type(self, data, keys):
        """Get a list of bad data key type values"""
        bad_keys = []
        for key in keys:
            if type(data[key]) is not str:
                bad_keys.append('{} has unexpected data type'.format(key))
        return bad_keys

    def has_empty_feilds(self, data, keys):
        """ get list of keys with missing data"""
        empty_fields = []
        for key in keys:
            if len(data[key]) == 0:
                empty_fields.append('{} is empty'.format(key))
        return empty_fields

    def has_bad_name(self, data, names):
        """Check if name contains special characters"""
        empty_fields = []
        for name in names:
            if re.search("[$#@]", data[name]) or (
                                re.search("[0-9]", data[name])):
                empty_fields.append('{} can only contain letters'.format(name))
        return empty_fields

    def has_bad_phone_number(self, phone_number):
        if re.search("[a-zA-Z]", phone_number):
            return 'phone number is wrong'

    def has_proper_email(self, email):
        pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, email):
            return 'email is wrong'.format(email)

