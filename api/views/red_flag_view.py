from api import app, jwt
from api.controllers.incident_controller import IncidentController
from flask import request, jsonify
from flask_jwt_extended import jwt_required


incident_controller = IncidentController()
incident_type = 'red-flag'


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'greeting': 'Welcome to iReporter',
        'post incident': '/api/v1/redflags',
        'get incidents': '/api/v1/redflags',
        'get incident': '/api/v1/redflags/flag_id',
        'alter incident': '/api/v1/redflags/flag_id',
        'update incident': '/api/v1/redflags/flag_id/key',
        'delete incident': '/api/v1/redflags/flag_id'
    }), 200


@app.route('/api/v1/incidents', methods=['POST'])
@jwt_required
def create_incident():
    return incident_controller.create_incident()


@app.route('/api/v1/redflags', methods=['GET'])
@jwt_required
def get_incidents():

    return incident_controller.get_incidents(incident_type)


@app.route('/api/v1/redflags/<int:incident_id>',
           methods=['GET'])
@jwt_required
def get_incident(incident_id):

    return incident_controller.get_incident(incident_type, incident_id)
