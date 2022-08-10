from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
con = 'mysql+pymysql://root:mypass123@localhost/sql_marsh'
app.config['SQLALCHEMY_DATABASE_URI'] = con

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reward_name = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='rewards')


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class RewardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reward


db.create_all()


@app.route('/')
def index():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(users)
    print(type(output))
    return jsonify({'user': output})


if __name__ == '__main__':
    app.run(debug=True)
