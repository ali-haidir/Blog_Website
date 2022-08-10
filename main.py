from flask import Flask, render_template, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime, date
import os
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret string here'

con = 'mysql+pymysql://root:mypass123@localhost/flask_r'
app.config['SQLALCHEMY_DATABASE_URI'] = con

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route('/')
def home():
    return "Hello World"


# for many to many relationships we need a new table
actors = db.Table('actors',
                  db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
                  db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
                  )


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80))
#     email = db.Column(db.String(80))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))

    release_date = db.Column(db.DateTime)

# to relate movies to director for one 2 many relationship
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))

# to relate movies to actors for many to many relationship
    actors = db.relationship("Actor", secondary=actors,
                             backref='movies', lazy='select')

    def release_year(self):
        return self.release_date.strftime("%Y")


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

# defining one 2 many relationship
# between Dieector and Movies
# define the relation in director class

    movies = db.relationship(
        'Movie', backref=db.backref("director", lazy="joined"), lazy='select'
    )

# defining one 2 one relationship
# between Dieector and guild
# define the relation in director class
    guild = db.relationship(
        'Guildmembership',
        backref='director',
        lazy='select',
        uselist=False
    )


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    guild = db.relationship(
        "Guildmembership", backref="actor", lazy="select", uselist=False
    )


class Guildmembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guild = db.Column(db.String(255))

    # to relate movies to director for one 2 many relationship
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))

    actor_id = db.Column(db.Integer, db.ForeignKey("actor.id"))


# defining one 2 many relationship
# between Dieector and Movies
# define the relation in one class

# /---------------------------------------------\

@app.cli.command("initdb")
def reset_db():
    """Drops and Creates fresh database"""
    db.drop_all()
    db.create_all()

    print("Initialized default DB")


@app.cli.command("bootstrap")
def bootstrap_data():
    """Populates database with data"""

    db.drop_all()
    print("droping all the tables")

    db.create_all()

    m = Movie(
        title="Evil Dead", release_date=datetime.strptime("Oct 15 1981", "%b %d %Y")
    )

    m2 = Movie(
        title="Darkman", release_date=datetime.strptime("Aug 24 1990", "%b %d %Y")
    )

    m3 = Movie(
        title="The Quick and the Dead",
        release_date=datetime.strptime("Feb 10 1995", "%b %d %Y"),
    )

    m4 = Movie(
        title="The Gift", release_date=datetime.strptime("Jan 19 2001", "%b %d %Y")
    )

    m5 = Movie(
        title="Army of Darkness",
        release_date=datetime.strptime("Feb 19 1993", "%b %d %Y"),
    )

    db.session.add(m)
    db.session.add(m2)
    db.session.add(m3)
    db.session.add(m4)
    db.session.add(m5)

    d = Director(
        first_name="Sam", last_name="Raimi", guild=Guildmembership(guild="Raimi DGA")
    )
    m.director = d
    m2.director = d
    m3.director = d
    m4.director = d
    m5.director = d
    db.session.add(d)

    bruce = Actor(
        first_name="Bruce",
        last_name="Campbell",
        guild=Guildmembership(guild="Campbell SAG"),
    )
    ellen = Actor(
        first_name="Ellen",
        last_name="Sandweiss",
        guild=Guildmembership(guild="Sandweiss SAG"),
    )
    hal = Actor(
        first_name="Hal",
        last_name="Delrich",
        guild=Guildmembership(guild="Delrich SAG"),
    )
    betsy = Actor(
        first_name="Betsy", last_name="Baker", guild=Guildmembership(guild="Baker SAG")
    )
    sarah = Actor(
        first_name="Sarah", last_name="York", guild=Guildmembership(guild="York SAG")
    )

    # darkman actors
    liam = Actor(
        first_name="Liam", last_name="Neeson", guild=Guildmembership(guild="Neeson SAG")
    )
    frances = Actor(
        first_name="Frances",
        last_name="McDormand",
        guild=Guildmembership(guild="McDormand SAG"),
    )

    # Quick and the Dead Actors
    sharon = Actor(
        first_name="Sharon", last_name="Stone", guild=Guildmembership(guild="Stone Sag")
    )
    gene = Actor(
        first_name="Gene",
        last_name="Hackman",
        guild=Guildmembership(guild="Hackman Sag"),
    )

    # The Gift Actors
    cate = Actor(
        first_name="Cate",
        last_name="Blanchett",
        guild=Guildmembership(guild="Blanchett Sag"),
    )
    keanu = Actor(
        first_name="Keanu",
        last_name="Reeves",
        guild=Guildmembership(guild="Reeves Sag"),
    )

    db.session.add(bruce)
    db.session.add(ellen)
    db.session.add(hal)
    db.session.add(betsy)
    db.session.add(sarah)
    db.session.add(liam)
    db.session.add(frances)
    db.session.add(sharon)
    db.session.add(gene)
    db.session.add(cate)
    db.session.add(keanu)

    m.actors.extend((bruce, ellen, hal, betsy, sarah))
    m2.actors.extend((bruce, liam, frances))
    m3.actors.extend((bruce, sharon, gene))
    m4.actors.extend((bruce, cate, keanu))
    m5.actors.append(bruce)

    db.session.commit()

    print("Added development dataset")


if __name__ == '__main__':
    app.run(debug=True)
