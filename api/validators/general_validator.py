"""
Module to handle input validations
"""

import re
from flask import jsonify
from api.database.engine import DbConnection
from api.validators.validation_helper import ValidationHelpers

db_services = DbConnection()
validate = ValidationHelpers()


def validate_incident(data):
    '''
    Function to check if incident keys and key data is present
    Also checks if data is in required format
    Returns True on success otherwise False

    '''
    keys = ['title', 'comment', 'latitude', 'longitude', 'type', 'status']
    errors = validate.key_exists(data, keys)
    if errors:
        return errors

    keys = ['title', 'comment', 'type', 'status']
    errors = validate.key_value_not_empty(data, keys)
    if errors:
        return errors

    keys = ['title', 'comment', 'type', 'status']
    errors = validate.is_of_type_string(data, keys)
    if errors:
        return errors

    media_keys = ['images', 'videos']
    errors = validate.is_of_type_list(data, media_keys)
    if errors:
        return errors

    errors = validate.list_content_is_of_type_string(data, media_keys)
    if errors:
        return errors

    errors = validate.is_of_proper_media_format(data, media_keys)
    if errors:
        return errors

    errors = validate.is_proper_incident_type(data['type'])
    if errors:
        return errors

    errors = validate.is_proper_status(data['status'])
    if errors:
        return errors


def validate_user(data):
    '''
    Function to check if user keys and key data is present
    Also checks if data is in required format
    Returns True on success otherwise False

    '''
    keys = ['user_name', 'password', 'first_name',
            'last_name', 'email', 'phone_number',
            'is_admin', 'other_names']
    errors = validate.key_exists(data, keys)
    if errors:
        return errors

    keys = ['user_name', 'password', 'first_name',
            'last_name', 'email', 'phone_number', 'other_names']
    errors = validate.is_of_type_string(data, keys)
    if errors:
        return errors

    keys = ['user_name', 'password', 'first_name',
            'last_name', 'email', 'phone_number']
    errors = validate.key_value_not_empty(data, keys)
    if errors:
        return errors

    errors = validate.is_proper_email(data['email'])
    if errors:
        return errors

    errors = validate.is_proper_phone_number(data['phone_number'])
    if errors:
        return errors

    keys = ['first_name', 'last_name', 'other_names']
    errors = validate.is_proper_name(data, keys)
    if errors:
        return errors

    errors = validate.is_poper_password(data['password'])
    if errors:
        return errors


def validate_login(data):
    '''
    Function to check if the login data is present
    Returns True on success otherwise False

    '''
    keys = ['email', 'password']

    errors = (validate.key_exists(data, keys))
    if errors:
        return errors

    errors = (validate.is_of_type_string(data, keys))
    if errors:
        return errors

    errors = (validate.key_value_not_empty(data, keys))
    if errors:
        return errors


def is_modifiable(incident, user_id):
    '''
    Function to check if an incident is modifiable
    An incident is only modifiable if its status is pending
    Returns False if an incident is not modifiable

    '''
    user = db_services.get_user_by_id(user_id)

    if user is None:
        return 'authorization terminated'
    if user['isadmin'] is False:
        if not is_owner(incident, user_id):
            return 'incident belongs to another user'
        if not incident.status == "pending":
            return 'incident no longer modifiable'


def is_owner(incident, user_id):
    '''
    Function to check if an incident was created by a given user
    Returns False if the user is not the incident creator

    '''
    if incident.createdby != user_id:
        return False
    return True


def is_duplicate_email(email):
    user = db_services.get_user_by_email(email)
    if user:
        return True
    return False
