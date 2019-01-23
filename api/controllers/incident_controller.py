from api import app, jwt
from flask import Flask, request, json, jsonify, abort
from flask_jwt_extended import get_jwt_identity
from api.validators.Incident_Validator import ValidateIncident
from api.models.incident_model import Incident
from api.models.user_model import User
from api.models.db import DbConnection


incident_validator = ValidateIncident()
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
        user_id = get_jwt_identity()

        incident_body['created_by'] = user_id
        incident_body['status'] = 'Pending'

        if not incident_validator.has_required_keys(incident_body):
            abort(400)

        incident_type = incident_body['type']

        incident = Incident(**incident_body)
        db_services.insert_incident(incident)

        success_response = {
            'id': 1,
            'message': 'Created {} record'.format(incident_type)
        }

        return jsonify({'status': 201, 'data': [success_response]}), 201

    def get_incidents(self, incident_type):
        '''
        Function to retun all incident given an incident id

        '''
        user_id = get_jwt_identity()

        user = db_services.get_user_by_id(user_id)

        incidents = db_services.get_all_incidents(
                    user_id, user['isadmin'], incident_type
                    )

        return jsonify({'status': 200, 'data': [incidents]})
