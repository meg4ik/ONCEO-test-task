from src import db
from enum import Enum
from datetime import datetime

class Item(db.Model):

    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    color = db.Column(db.String(40), nullable=False)
    weigth = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    order_item_to = db.relationship("OrderItem", backref='item',lazy=True)


class OrderStatus(Enum):
    COMPLETED = 'виконано'
    CANCELED = 'відмінено'
    PROCESSING = 'обробляється'


class Order(db.Model):

    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Enum(OrderStatus), nullable=False)

    order_item_to = db.relationship("OrderItem", backref='order',lazy=True)
    order_address_to = db.relationship("AddressNode", backref='order',lazy=True)


class OrderItem(db.Model):

    __tablename__ = "order_item"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    item_id = db.Column(db.ForeignKey('item.id'), primary_key=True)
    order_id = db.Column(db.ForeignKey('order.id'), primary_key=True)
    count = db.Column(db.Integer, default=1)

class AddressNode(db.Model):

    __tablename__ = "address_node"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(36), nullable=False)
    prev_node = db.Column(db.Integer, default=None)
    order_id = db.Column(db.ForeignKey('order.id'), primary_key=True)


