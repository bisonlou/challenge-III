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


@app.route('/api/v1/interventions/<int:incident_id>', methods=['PUT'])
@jwt_required
@admin_denied
@json_data_required
def alter_intervention(incident_id):

    return incident_controller.put_incident(incident_id)


@app.route('/api/v1/interventions/<int:incident_id>/location',
           methods=['PATCH'])
@jwt_required
@admin_denied
@json_data_required
def patch_intervention_location(incident_id):

    return incident_controller.patch_incident(incident_id,
                                              incident_type, 'location')


@app.route('/api/v1/interventions/<int:incident_id>/comment',
           methods=['PATCH'])
@jwt_required
@admin_denied
@json_data_required
def patch_intervention_comment(incident_id):

    return incident_controller.patch_incident(incident_id,
                                              incident_type, 'comment')


@app.route('/api/v1/iterventions/<int:incident_id>', methods=['DELETE'])
@jwt_required
@admin_denied
def delete_intervention(incident_id):

    return incident_controller.delete_incident(incident_type, incident_id)
