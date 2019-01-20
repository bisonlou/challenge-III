from api import app
from flask import jsonify


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'status': 400, 'error': 'Bad Request'}), 400

@app.errorhandler(409)
def conflict(error):
    return jsonify({'status': 409, 'error': 'Confict'}), 409
