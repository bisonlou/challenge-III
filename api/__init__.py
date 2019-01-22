from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)

test_client = app.test_client()
app.config['SECRET_KEY'] = 'askjfskdkjvisewkjsdvkj876k,.'

import api.models.db
import api.views.user_view
import api.views.red_flag_view
import api.views.error_view
import api.models.user_model


