from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_security import Security, SQLAlchemyUserDatastore
from os import path

from flask_admin.contrib.sqla import ModelView

from .config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, SECRET, SECURITY_PASSWORD_SALT

temp_dir = path.abspath(path.dirname(__file__))

app = Flask(__name__, template_folder=path.join(temp_dir, 'templates'))

app.config['SECRET_KEY'] = SECRET
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT

app.config['DEBUG'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .admin_view import OrderItemModelView, OrderModelView, ItemModelView, AdressModelView
admin = Admin(app, name='My Admin', template_mode='bootstrap3')

from .database.models import Item, Order, OrderItem, User, Role, AddressNode

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(OrderItemModelView(OrderItem, db.session))
admin.add_view(OrderModelView(Order, db.session))
admin.add_view(ItemModelView(Item, db.session))
admin.add_view(AdressModelView(AddressNode, db.session))


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from . import resources
from .database import models