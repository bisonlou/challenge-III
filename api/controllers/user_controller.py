from api import app
from datetime import datetime
from api.models.user_model import User
from api.database.engine import DbConnection
from flask import jsonify, abort, request
from api.utility.authenticator import (
    create_access_token,
    get_identity,
    verify_is_admin)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash)
from api.validators.general_validator import (
    validate_login,
    validate_user,
    is_duplicate_email)


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

        errors = validate_user(data)
        if errors:
            return jsonify({'status': 400, 'errors': errors}), 400

        if is_duplicate_email(data['email']):
            return jsonify({'status': 409, 'errors': [
                            'User already registered']}), 409

        hashed_password = generate_password_hash(
            data['password'], method='sha256')

        data['date_registered'] = dteRegistered = datetime.utcnow().date()
        data['password'] = hashed_password

        new_user = User(**data)
        user = db_services.add_user(new_user)
        del user['password']

        access_token = create_access_token(user['id'], user['isadmin'])
        success_response = {'user': user,
                            'message': 'User created',
                            'access_token': access_token}
        
        return jsonify({'status': 201, 'data': [success_response]}), 201

    def login(self):
        """
        Function to login a user
        The user must be registered
        The function returns a json web token
        """

        data = request.get_json()

        errors = validate_login(data)
        if errors:
            return jsonify({'status': 400, 'errors': errors}), 400

        user = db_services.get_user_by_email(data['email'])

        if user is None:
            return jsonify({'status': 401, 'errors':
                            ['There are problems with your login']}), 401

        if check_password_hash(user['password'], data['password']):
            access_token = create_access_token(user['id'], user['isadmin'])
            del user['password']

            success_response = {'user': user,
                                'access_token': access_token}
            return jsonify({'status': 200, 'data': [success_response]}), 200

        return jsonify({'status': 401, 'errors': ['There are problems with your login']}), 401     

    def get_users(self):
        """
        Function to get a list of users
        Only admins permisable
        """
        users = db_services.get_users()    
        return jsonify({'status': 200, 'data': [users]}), 200

    def get_user(self):
        """
        The function returns a user
        """
        user_id = get_identity()
        user = db_services.get_user_by_id(user_id)    
        return jsonify({'status': 200, 'data': [user]}), 200
        
    