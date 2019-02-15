"""
Module to handle incident CRUD operations
"""
import os
from api import app
from datetime import datetime
from api.models.user_model import User
from werkzeug.utils import secure_filename
from api.database.engine import DbConnection
from api.models.incident_model import Incident
from api.utility.authenticator import get_identity
from api.validators.general_validator import(
    validate_incident,
    is_modifiable,
    is_owner
)
from flask import Flask, request, json, jsonify, abort


db_services = DbConnection()


class IncidentController():
    '''
    Class to handle incident related routes
    '''

    def create_incident(self):
        '''
        Function to create an incident
        Validates the incident data
        If data passes validation an incident is created

        '''
        incident_body = request.get_json()
        user_id = get_identity()

        incident_body['createdby'] = user_id
        incident_body['status'] = 'pending'
        incident_body['createdon'] = datetime.utcnow().date()

        errors = validate_incident(incident_body)
        if errors:
            return jsonify({'status': 400, 'errors': errors}), 400

        incident_type = incident_body['type']
        images = self.get_media(incident_body, 'images')
        videos = self.get_media(incident_body, 'videos')

        incident = Incident(**incident_body)

        self.add_incident_media(incident, images, 'images')
        self.add_incident_media(incident, videos, 'videos')

        incident_id = db_services.insert_incident(incident)

        success_response = {
            'id': incident_id,
            'message': 'Created {} record'.format(incident_type)
        }

        return jsonify({'status': 201, 'data': [success_response]}), 201

    def get_incidents(self, incident_type):
        '''
        Function to retun all incident given an incident id
        '''
        user_id = get_identity()

        incidents = db_services.get_all_incidents(user_id, incident_type)

        incident_totals = db_services.get_user_totals(
                            user_id, incident_type)

        return jsonify({'status': 200, 'data': [incidents],
                       'totals': incident_totals})

    def get_incident(self, incident_id):
        '''
        Function to retun an incident give an incident id
        Validates the incident exists and belongs to this user
        If validation is passed an incident is returned

        '''
        user_id = get_identity()
        incident = db_services.get_incident(incident_id)

        if not incident:
            return jsonify({'status': 404, 'errors':
                            'Incident does not exist'}), 404

        return jsonify({'status': 200, 'data': [incident.to_dict()]}), 200

    def put_incident(self, incident_id):
        '''
        Function to update an entire incident
        Validates the incident exists and belongs to this user
        If validation is passed the incident is updated
        and the updted incident is returned

        '''
        data = request.get_json()
        user_id = get_identity()

        data['created_by'] = user_id
        data['id'] = incident_id

        errors = validate_incident(data)
        if errors:
            return jsonify({'status': 400, 'errors': errors}), 400

        current_incident = db_services.get_incident(incident_id)
        if current_incident is None:
            return jsonify({'status': 404, 'errors':
                            'incident not found'}), 404

        error = is_modifiable(current_incident, user_id)
        if error:
            return jsonify({'status': 403, 'errors': error}), 403

        update_incident = Incident(**data)

        updated_incident = db_services.put_incident(update_incident)

        return jsonify({
            'status': 200,
            'data': [updated_incident.to_dict()]
            })

    def patch_incident(self, incident_id, update_key):
        '''
        Function to update a property of an incident
        Validates the incident exists and belongs to this user
        If validation is passed the incidentpropert is updated
        and a success message is returned

        '''
        data = request.get_json()
        user_id = get_identity()

        data['created_by'] = user_id
        data['id'] = incident_id

        errors = validate_incident(data)
        if errors:
            return jsonify({'status': 400, 'errors': errors}), 400

        existing_incident = db_services.get_incident(incident_id)

        if not existing_incident:
            return jsonify({'status': 404, 'errors':
                            'incident not found'}), 404

        incident_type = existing_incident.type

        errors = is_modifiable(existing_incident, user_id)
        if errors:
            return jsonify({'status': 403, 'error': errors}), 403

        update_incident = Incident(**data)

        incident = db_services.patch_incident(
            update_incident, update_key)
        success_response = {
            'id': incident_id,
            'message':
            'Updated {} record’s {}'.format(incident_type, update_key)
        }

        return jsonify({'status': 200, 'data': [success_response]}), 200

    def patch_incident_image(self, incident_id):
        user_id = get_identity()      
        APP_ROOT = os.path.dirname(os.path.abspath('api/'))
        upload_folder = os.path.join(APP_ROOT, os.environ['UPLOAD_FOLDER'])
                                    
        incident = db_services.get_incident(incident_id)
        if not incident:
            return jsonify({'status': 404, 'errors':
                            'incident not found'}), 404

        errors = is_modifiable(incident, user_id)
        if errors:
            return jsonify({'status': 403, 'error': errors}), 403

        incident_type = incident.type

        image = request.files.get('image', '')
        if image.filename == '':
            return jsonify({'status': 400, 'errors':
                        ['image name cannot be empty']}), 400

        filename = secure_filename(image.filename)
        image.save(os.path.join(upload_folder, filename))

        db_services.add_incident_image(incident_id, filename)
            
        success_response = {
            'id': incident_id,
            'message':
            'Image added to {} record'.format(incident_type)
            }

        return jsonify({'status': 201, 'data': [success_response]}), 201

    def delete_incident(self, incident_id):
        '''
        Function to delete an incident
        Validates the incident exists and belongs to this user
        or the user is an admin
        If validation is passed the incident is deleted
        and a success message is returned

        '''
        user_id = get_identity()

        user = db_services.get_user_by_id(user_id)
        if not user:
            return jsonify({'status': 401, 'errors':
                            'You are not authenticated'}), 401

        existing_incident = db_services.get_incident(incident_id)

        if existing_incident is None:
            return jsonify({'status': 404, 'error':
                            'Incident doesnt exist'}), 404

        errors = is_modifiable(existing_incident, user_id)
        if errors:
            return jsonify({'status': 403, 'error': errors}), 403

        incident_type = existing_incident.type

        deleted_id = db_services.delete_incident(existing_incident.id)
        if deleted_id is None:
            return jsonify({'status': 404, 'error':
                            'Incident doesnt exist'}), 404

        success_response = {
            'id': deleted_id,
            'message':
            '{} record has been deleted'.format(incident_type)
        }

        return jsonify({'status': 200, 'data': success_response}), 200

    def get_media(self, incident, media_type):
        if media_type in incident:
            return incident[media_type]

    def add_incident_media(self, incident, media_list, media_type):
        if media_list:
            for media in media_list:
                if media_type == 'images':
                    incident.add_image(media)
                elif media_type == 'videos':
                    incident.add_video(media)
