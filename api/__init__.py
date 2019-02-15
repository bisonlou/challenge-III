from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

test_client = app.test_client()

import api.database.engine
import api.views.user_view
import api.views.red_flag_view
import api.views.common_routes
import api.views.intervention_view
import api.models.user_model


