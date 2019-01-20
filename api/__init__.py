from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:system#2008@localhost/ireporter'
db = SQLAlchemy(app)


test_client = app.test_client()

import api.views.user_view
import api.views.error_view

