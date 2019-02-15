from api import app
from api.utility.authenticator import json_data_required
from api.controllers.user_controller import UserController
from api.utility.authenticator import (jwt_required, admin_required)


user_controller = UserController()


@app.route('/api/v1/auth/signup', methods=['POST'])
@json_data_required
def register():
    return user_controller.register()


@app.route('/api/v1/auth/login', methods=['POST'])
@json_data_required
def login():
    return user_controller.login()

@app.route('/api/v1/auth/users', methods=['GET'])
@jwt_required
@admin_required
def get_users():
    return user_controller.get_users()

@app.route('/api/v1/auth/user', methods=['GET'])
@jwt_required
def get_user():
    return user_controller.get_user()
