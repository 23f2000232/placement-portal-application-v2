from flask import Flask

from app.routes.admin.admin_controller import admin_bp
from app.routes.auth.auth_controller import auth_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)