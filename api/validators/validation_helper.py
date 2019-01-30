import re


class ValidationHelpers():

    def key_exists(self, data, keys):
        """Get missing keys in a list"""
        missing_keys = []
        for key in keys:
            if key not in data:
                missing_keys.append('{} key missing'.format(key))
        return missing_keys

    def is_of_type_string(self, data, keys):
        """Get a list of bad data key type values"""
        bad_keys = []
        for key in keys:
            if type(data[key]) is not str:
                bad_keys.append('{} has should be of type string'.format(key))
        return bad_keys

    def is_of_type_list(self, data, keys):
        media_errors = []
        sent_media = [key for key in keys if key in data]

        for media in sent_media:
            if type(data[media]) is not list:
                media_errors.append('{} has should be in a list'.format(media))

        return media_errors

    def list_content_is_of_type_string(self, data, media_keys):
        media_key_list = [key for key in media_keys if key in data]
        for key in media_key_list:
            for index in range(len(data[key])):
                if type(data[key][index]) is not str:
                    return 'list contents should be strings'

    def is_of_proper_media_format(self, data, media_keys):
        media_key_list = [key for key in media_keys if key in data]
        for key in media_key_list:
            for index in range(len(data[key])):
                pattern = '([^\\s]+(\\.(?i)(jpg|png|gif|bmp|mp4|mov|3gp))$)'
                if not re.match(pattern, data[key][index]):
                    return '''unexpected media format, expected one of
                    jpg|png|gif|bmp|mp4|mov|3gp'''

    def key_value_not_empty(self, data, keys):
        """ get list of keys with missing data"""
        empty_fields = []
        for key in keys:
            if len(data[key]) == 0:
                empty_fields.append('{} is required'.format(key))
        return empty_fields

    def is_proper_incident_type(self, incident_type):
        incident_type_errors = []
        accepted_incident_types = ['red-flag', 'intervention']
        if incident_type not in accepted_incident_types:
            return 'incident type unknown'

    def is_proper_status(self, status):
        status_errors = []
        accepted_status_values = ['pending', 'under investigation',
                                  'resolved', 'rejected']
        if status not in accepted_status_values:
            return 'status unknown'

    def is_poper_password(self, password):
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

    def is_proper_name(self, data, names):
        """Check if name contains special characters"""
        empty_fields = []
        for name in names:
            if re.search("[$#@]", data[name]) or (
                                re.search("[0-9]", data[name])):
                empty_fields.append('{} can only contain letters'.format(name))
        return empty_fields

    def is_proper_phone_number(self, phone_number):
        if re.search("[a-zA-Z]", phone_number):
            return 'phone number is wrong'

    def is_proper_email(self, email):
        pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, email):
            return 'email is wrong'.format(email)

