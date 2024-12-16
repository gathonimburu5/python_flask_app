from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

