from flask import request, jsonify
from api import app
from api.controllers.incident_controller import IncidentController
from api.utility.authenticator import jwt_required


incident_controller = IncidentController()
incident_type = 'red-flag'


@app.route('/api/v1/redflags', methods=['GET'])
@jwt_required
def get_incidents():

    return incident_controller.get_incidents(incident_type)

