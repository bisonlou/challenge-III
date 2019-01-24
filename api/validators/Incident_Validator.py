from flask import jsonify


class ValidateIncident():

    def has_required_keys(self, data):
        '''
        Function to check if incident keys and key data is present
        Also checks if data is in required format
        Returns True on success otherwise False

        '''
        keys = ['title', 'comment', 'location', 'type']
        missing_keys = self.has_missing_keys(data, keys)
        if len(missing_keys) > 0:
            return missing_keys

        keys = ['title', 'comment', 'type']
        bad_data = self.has_unexpected_data_type(data, keys)
        if len(bad_data) > 0:
            return bad_data

        keys = ['title', 'comment', 'location', 'type']
        empty_fields = self.has_empty_feilds(data, keys)
        if len(empty_fields) > 0:
            return empty_fields

        keys = ['images', 'videos']
        media_errors = self.has_bad_media(data, keys)
        if media_errors:
            return media_errors

        # media_data = [data['images'], data['videos']]
        # media_content_errors = self.has_bad_media_content(media_data)
        # if media_content_errors:
        #     return media_content_errors

        incident_type_errors = self.has_bad_incident_type(data['type'])
        if incident_type_errors:
            return incident_type_errors

    def has_missing_keys(self, data, keys):
        """Get missing keys in a list"""
        missing_keys = []
        for key in keys:
            if key not in data:
                missing_keys.append('{} key missing'.format(key))
        return missing_keys

    def has_unexpected_data_type(self, data, keys):
        """Get a list of bad data key type values"""
        bad_keys = []
        for key in keys:
            if type(data[key]) is not str:
                bad_keys.append('{} has should be of type string'.format(key))
        return bad_keys

    def has_bad_media(self, data, keys):
        media_errors = []
        sent_media = [key for key in keys if key in data]

        for media in sent_media:
            if type(data[media]) is not list:
                media_errors.append('{} has should be in a list'.format(media))

        return media_errors

    # def has_bad_media_content(self, media_list):
    #     bad_content = [media for media in media_list if type(media) is not str]
    #     if len(bad_media) > 0:
    #         return 'list contents should be strings'

    def has_empty_feilds(self, data, keys):
        """ get list of keys with missing data"""
        empty_fields = []
        for key in keys:
            if len(data[key]) == 0:
                empty_fields.append('{} is required'.format(key))
        return empty_fields

    def has_bad_incident_type(self, incident_type):
        incident_type_errors = []
        accepted_incident_types = ['red-flag', 'intervention']
        if incident_type not in accepted_incident_types:
            return 'incident type unknown'

    def is_modifiable(self, incident):
        '''
        Function to check if an incident is modifiable
        An incident is only modifiable if its status is pending
        Returns False if an incident is not modifiable

        '''
        if not incident['status'] == "Pending":
            return False
        return True

    def is_owner(self, incident, user_id):
        '''
        Function to check if an incident was created by a given user
        Returns False if the user is not the incident creator

        '''
        if incident['createdby'] != user_id:
            return False
        return True
