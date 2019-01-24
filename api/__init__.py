from flask import Flask

app = Flask(__name__)

test_client = app.test_client()

import api.models.db
import api.views.user_view
import api.views.red_flag_view
import api.views.error_view
import api.models.user_model


