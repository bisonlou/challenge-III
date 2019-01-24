from api import app
from api.utility.authenticator import json_data_required
from api.controllers.user_controller import UserController

user_controller = UserController()


@app.route('/api/v1/auth/signup', methods=['POST'])
@json_data_required
def register():
    return user_controller.register()

@app.route('/api/v1/auth/login', methods=['POST'])
@json_data_required
def login():
    return user_controller.login()

