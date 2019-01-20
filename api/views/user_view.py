from api import app
from api.controllers.user_controller import UserController

user_controller = UserController()


@app.route('/api/v1/register', methods=['POST'])
def register_user():

    return user_controller.register()


