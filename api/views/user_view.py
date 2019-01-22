from api import app
from api.controllers.user_controller import UserController

user_controller = UserController()


@app.route('/api/v1/auth/signup', methods=['POST'])
def register():
    return user_controller.register()

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    return user_controller.login()


