from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from os import path
from celery import Celery

from flask_admin.contrib.sqla import ModelView
from flask_jsonrpc import JSONRPC

from flask_login import LoginManager, login_user, logout_user, login_required

from .config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, SECRET, SECURITY_PASSWORD_SALT,REDIS_HOST, REDIS_PORT

temp_dir = path.abspath(path.dirname(__file__))

app = Flask(__name__, template_folder=path.join(temp_dir, 'templates'))

app.config['SECRET_KEY'] = SECRET
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT

app.config['DEBUG'] = False

from src import celery_config

celery = Celery(app.name)
celery.config_from_object(celery_config)

jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .admin_view import OrderItemModelView, OrderModelView, ItemModelView, AdressModelView, UserModelView, RoleModelView
admin = Admin(app, name='My Admin', template_mode='bootstrap3')

from .database.models import Item, Order, OrderItem, User, Role, AddressNode

admin.add_view(UserModelView(User, db.session))
admin.add_view(RoleModelView(Role, db.session))
admin.add_view(OrderItemModelView(OrderItem, db.session))
admin.add_view(OrderModelView(Order, db.session))
admin.add_view(ItemModelView(Item, db.session))
admin.add_view(AdressModelView(AddressNode, db.session))

from .forms import LoginForm

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()

from . import resources
from .database import models