import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST=os.environ.get("MYSQL_HOST")
MYSQL_PORT=os.environ.get("MYSQL_PORT")
MYSQL_DB=os.environ.get("MYSQL_DB")
MYSQL_USER=os.environ.get("MYSQL_USER")
MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD")

SECRET=os.environ.get("SECRET")

REDIS_HOST=os.environ.get("REDIS_HOST")
REDIS_PORT=os.environ.get("REDIS_PORT")

SECURITY_PASSWORD_SALT=os.environ.get("SECURITY_PASSWORD_SALT")