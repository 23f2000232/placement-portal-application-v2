from dotenv import load_dotenv
from flask import Flask

from app.config import Config
from app.extensions import bcrypt, cors, db, jwt
from app.logging_config import configure_logging
from app.models import *
from app.seed import seed_admin


def create_app() -> Flask:
    load_dotenv()
    configure_logging()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    with app.app_context():
        db.create_all()
        seed_admin()

    return app