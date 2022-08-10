from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

con = 'mysql+pymysql://root:mypass123@localhost/flask_r'
app.config['SQLALCHEMY_DATABASE_URI'] = con

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
