from datetime import datetime
from api import app
from api.models.user_model import User
from api.models.db import DbConnection
from api.validators.user_validator import UserValidator
from api.utility.authenticator import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, abort, request

validator = UserValidator()
db_services = DbConnection()


class UserController():
    '''
    Class to handle user related routes

    '''

    def register(self):
        '''
        Function to register a user
        '''
        data = request.get_json()

        errors = validator.has_required_fields(data)
        if errors:
            return jsonify({'status': 400, 'errors': errors}), 400

        if validator.Check_for_duplicate_email(data['email']):
            return jsonify({'status': 409, 'errors':
                            'Conflict: user already registered'}), 409

        hashed_password = generate_password_hash(
            data['password'], method='sha256')

        data['date_registered'] = dteRegistered = datetime.utcnow().date()
        data['password'] = hashed_password

        new_user = User(**data)
        user = db_services.add_user(new_user)

        success_response = {'user': user, 'message': 'User created'}
        return jsonify({'status': 201, 'data': [success_response]}), 201

    def login(self):
        """
        Function to login a user
        The user must be registered
        The function returns a json web token
        """

        data = request.get_json()

        errors = validator.has_login_required_fields(data)
        if errors:
            return jsonify({'status': 400, 'errors': errors}), 400

        user = db_services.get_user_by_email(data['email'])

        if user is None:
            return jsonify({'status': 401, 'error':
                            'incorrect credentials'}), 401

        if check_password_hash(user['password'], data['password']):
            access_token = create_access_token(user['id'], user['isadmin'])
            success_response = {'user': user,
                                'access_token': access_token}
            return jsonify({'status': 200, 'data': [success_response]}), 200
        abort(401)
