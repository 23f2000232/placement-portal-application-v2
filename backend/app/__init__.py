from dotenv import load_dotenv
from flask import Flask

from app.config import Config
from app.extensions import bcrypt, cors, db, jwt
from app.models import *


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    with app.app_context():
        db.create_all()

    return app