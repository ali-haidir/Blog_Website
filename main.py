from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret string here'

con = 'mysql+pymysql://root:mypass123@localhost/flask_r'
app.config['SQLALCHEMY_DATABASE_URI'] = con

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


@app.route('/')
def home():
    return "Hello World,"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))


if __name__ == '__main__':
    app.run(debug=True)
