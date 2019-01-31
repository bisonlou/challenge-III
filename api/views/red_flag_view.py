from flask import request, jsonify
from api import app
from api.controllers.incident_controller import IncidentController
from api.utility.authenticator import (jwt_required, admin_denied,
                                       json_data_required, admin_required)


incident_controller = IncidentController()
incident_type = 'red-flag'


@app.route('/api/v1/redflags', methods=['GET'])
@jwt_required
def get_incidents():

    return incident_controller.get_incidents(incident_type)


@app.route('/api/v1/redflags/<int:incident_id>', methods=['GET'])
@jwt_required
def get_red_flag(incident_id):

    return incident_controller.get_incident(incident_type, incident_id)


@app.route('/api/v1/redflags/<int:incident_id>', methods=['DELETE'])
@jwt_required
@admin_denied
def delete_red_flag(incident_id):

    return incident_controller.delete_incident(incident_type, incident_id)
