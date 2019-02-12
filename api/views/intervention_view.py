from flask import request, jsonify
from api import app
from api.controllers.incident_controller import IncidentController
from api.utility.authenticator import (jwt_required, admin_denied,
                                       json_data_required)


incident_controller = IncidentController()
incident_type = 'intervention'


@app.route('/api/v1/interventions', methods=['GET'])
@jwt_required
def get_interventions():

    return incident_controller.get_incidents(incident_type)


@app.route('/api/v1/interventions/<int:incident_id>',
           methods=['GET'])
@jwt_required
def get_intervention(incident_id):

    return incident_controller.get_incident(incident_type, incident_id)
