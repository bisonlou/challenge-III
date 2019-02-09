from flask import request, jsonify
from api import app
from api.controllers.incident_controller import IncidentController
from api.utility.authenticator import (jwt_required, admin_denied,
                                       json_data_required, admin_required)

incident_controller = IncidentController()


@app.route('/', methods=['GET'])
def index():

    data = jsonify({
        'post incident': '/api/v1/incidents',
        'get red flags': '/api/v1/redflags',
        'get red flag': '/api/v1/redflags/<flag_id>',
        'get interventions': '/api/v1/interventions',
        'get intervention': '/api/v1/interventions/<intevention_id>',
        'put incident': '/api/v1/incidents/<incident_id>',
        'patch location': '/api/v1/incidents/<incident_id>/location',
        'patch incident comment': '/api/v1/incidents/<incident_id>/comment',
        'delete red flag': '/api/v1/redflags/<flag_id>',
        'delete intervention': '/api/v1/interventions/<intevention_id>',
        'patch status': '/api/v1/incidents/<incident_id>'
    }), 200

    response = app.make_response(data)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@app.route('/api/v1/incidents', methods=['POST'])
@jwt_required
@admin_denied
@json_data_required
def create_incident():
    """
    Endpoint to post incident
    """

    return incident_controller.create_incident()


@app.route('/api/v1/incidents/<int:incident_id>', methods=['PUT'])
@jwt_required
@admin_denied
@json_data_required
def alter_red_flag(incident_id):
    """
    Endpoint to alter incident
    """

    return incident_controller.put_incident(incident_id)


@app.route('/api/v1/incidents/<int:incident_id>/location', methods=['PATCH'])
@jwt_required
@admin_denied
@json_data_required
def patch_red_flag_location(incident_id):
    """
    Endpoint to patch incident comment
    """

    return incident_controller.patch_incident(incident_id, 'location')


@app.route('/api/v1/incidents/<int:incident_id>/comment', methods=['PATCH'])
@jwt_required
@admin_denied
@json_data_required
def patch_incident_comment(incident_id):
    """
    Endpoint to patch incident comment
    """

    return incident_controller.patch_incident(incident_id, 'comment')

@app.route('/api/v1/incidents/<int:incident_id>/addImage', methods=['PATCH'])
@jwt_required
@admin_denied
def add_image(incident_id):
    """
    Endpoint to add incident image
    """
    
    return incident_controller.patch_incident_image(incident_id)

@app.route('/api/v1/incidents/<int:incident_id>/status',
           methods=['PATCH'])
@jwt_required
@admin_required
@json_data_required
def patch_incident_status(incident_id):
    """
    Endpoint to delete incident
    """

    return incident_controller.patch_incident(incident_id, 'status')

@app.route('/api/v1/incidents/<int:incident_id>', methods=['DELETE'])
@jwt_required
@admin_denied
def delete_red_flag(incident_id):

    return incident_controller.delete_incident(incident_id)
