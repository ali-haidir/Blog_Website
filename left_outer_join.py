from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# select * from customer left join purchase on customer.id = purchase.customer_id

#db.session.query(Customer,Purchase).outerjoin(Purchase,Customer.id == Purchase.customer_id).all()
app = Flask(__name__)
con = 'mysql+pymysql://root:mypass123@localhost/left_join'
app.config['SQLALCHEMY_DATABASE_URI'] = con

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    orders = db.relationship('Purchase', backref='customer')


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    price = db.Column(db.Integer)


all = Customer.query.all()
print(all)

r = db.session.query(Customer, Purchase).outerjoin(
    Purchase, Customer.id == Purchase.customer_id).all()
for result in r:
    if result[1]:
        print('Name: {} Amount Paid: {}'.format(
            result[0].name, result[1].price))
    else:
        print('Name: {} did not make any Purchase'.format(result[0].name))

# #
# # r2 = db.session.query(Customer, Purchase).select_entity_from(
# #     Purchase,).join(Customer, isouter=True)
# r2 = db.session.query(Customer, Purchase).outerjoin(
#     Purchase, Purchase.id == Customer.purchase_id).all()
# r3 = db.session.query(Customer.name).Select_entity_from(select([Purchase.price]))\
#     .join(Customer, Customer.id == Purchase.customer_id)\
#     .filter(Purchase.id == my_id).first()
# print(r2)
