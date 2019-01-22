from flask import Flask

app = Flask(__name__)

test_client = app.test_client()
app.config['SECRET_KEY'] = 'askjfskdkjvisewkjsdvkj876k,.'

import api.views.user_view
import api.views.error_view
import api.models.user_model


