from .config import REDIS_HOST, REDIS_PORT
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

temp_dir = path.abspath(path.dirname(__file__))
app = Flask(__name__)

print(REDIS_HOST, REDIS_PORT)