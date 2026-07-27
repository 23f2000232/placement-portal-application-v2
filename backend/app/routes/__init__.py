from flask import Flask

from app.routes.admin.admin_controller import admin_bp
from app.routes.auth.auth_controller import auth_bp
from app.routes.company_controller import company_bp
from app.routes.student_controller import student_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)