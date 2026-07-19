# Create shared extension instances that can be initialized later with the Flask application.
# A registry of reusable Flask extensions.

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()