from flask import Flask
from config import Config
from flask_cors import CORS
from flask_login import LoginManager
import logging


logger = logging.getLogger('flask_cors')
logger.level = logging.DEBUG

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

from app import routes, models
