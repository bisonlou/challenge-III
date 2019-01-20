from datetime import datetime
from api import app, db
from api.models.user_model import User
from api.validators.user_validator import UserValidator
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, abort, request

validator = UserValidator()


class UserController():
    '''
    Class to handle user related routes

    '''

    def register(self):
        '''
        Function to register a user
        '''
        data = request.get_json()
        
        if not validator.has_required_fields(data):
            abort(400)

        if validator.duplicate_email(data['email']):
            abort(409)            
        
        errors = validator.get_password_errors(data)
        if len(errors) > 0:
            return jsonify({'status': 400, 'data': errors}), 400
        
        hashed_password = generate_password_hash(
                            data['password'], method='sha256')

        is_admin = False
        if User.query.count() == 0:
            is_admin = True

        new_user = User(userName = data['user_name'],
                        email = data['email'],
                        lastName = data['last_name'],
                        firstName = data['first_name'],
                        otherNames = data['other_names'],
                        password = hashed_password,
                        phoneNumber = data['phone_number'],
                        isAdmin = is_admin,
                        dteRegistered = datetime.utcnow().date()
                        )

        db.session.add(new_user)
        db.session.commit()

        user_id = User.query.filter_by(email=data['email']).first().id
        success_response = {'id': user_id, 'message': 'User created'}

        return jsonify({'status': 201, 'data': success_response}), 201
   