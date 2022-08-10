from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

con = 'mysql+pymysql://root:mypass123@localhost/marsh'
app.config['SQLALCHEMY_DATABASE_URI'] = con

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="books")


class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author

    id = ma.auto_field()
    name = ma.auto_field()
    books = ma.auto_field()

#
# class BookSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Book
#         include_fk = True


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

    author = ma.HyperlinkRelated("author_detail")


db.create_all()
db.drop_all()
author_schema = AuthorSchema()
book_schema = BookSchema()
author = Author(name="Chuck Paluhniuk")
book = Book(title="Fight Club", author=author)

with app.test_request_context():
    print(book_schema.dump(book))

db.session.add(author)
db.session.add(book)
db.session.commit()
print(author_schema.dump(author))
