from src import db
from enum import Enum
from datetime import datetime
from flask_security import UserMixin
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = OrderStatus.PROCESSING
        self.uuid = str(uuid.uuid4())


class OrderItem(db.Model):

    __tablename__ = "order_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), unique=True)
    item_id = db.Column(db.ForeignKey('item.id'), primary_key=True)
    order_id = db.Column(db.ForeignKey('order.id'), primary_key=True)
    count = db.Column(db.Integer, default=1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uuid = str(uuid.uuid4())

class AddressNode(db.Model):

    __tablename__ = "address_node"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(36), nullable=False)
    prev_node = db.Column(db.Integer, default=None)
    order_id = db.Column(db.ForeignKey('order.id'), primary_key=True)


