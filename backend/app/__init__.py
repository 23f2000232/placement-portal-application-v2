from dotenv import load_dotenv
from flask import Flask

from app.config import Config
from app.celery_app import init_celery
from app.extensions import bcrypt, cors, db, jwt
from app.handlers.exception_handler import register_exception_handlers
from app.logging_config import configure_logging
from app.models import *
from app.routes import register_routes
from app.seed import seed_admin


def create_app() -> Flask:
    load_dotenv()
    configure_logging()

    app = Flask(__name__)
    app.config.from_object(Config)
    init_celery(app)
    register_exception_handlers(app)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    with app.app_context():
        db.create_all()
        seed_admin()
        register_routes(app)

    return app
