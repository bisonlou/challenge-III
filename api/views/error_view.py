from api import app
from flask import jsonify


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'status': 400, 'error': 'Bad Request'}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'status': 401, 'error': 'Unauthorized'}), 401

@app.errorhandler(403)
def forbiden(error):
    return jsonify({'status': 403, 'error': 'Forbiden'}), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 404, 'error': 'Not Found'}), 404

@app.errorhandler(409)
def conflict(error):
    return jsonify({'status': 409, 'error': 'Confict'}), 409
