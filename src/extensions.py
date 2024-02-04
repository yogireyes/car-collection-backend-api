from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()