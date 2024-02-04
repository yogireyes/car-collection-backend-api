from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from config import Config

from src.extensions import db, login_manager, ma
from src.helpers import JSONEncoder

from src.authentication.routes import auth
from src.api.routes import api
from src.site.routes import site

app = Flask(__name__)
CORS(app, supports_credentials=True)
Bootstrap5(app)

app.register_blueprint(auth)
app.register_blueprint(api)
app.register_blueprint(site)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app,db)
