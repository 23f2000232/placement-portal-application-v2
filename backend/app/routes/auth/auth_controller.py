from http import HTTPStatus

from flask import jsonify, request, Blueprint

from app.decorators.role_decorators import authenticated_required
from app.dependencies import auth_service
from app.schemas.auth import (
    StudentRegistrationRequest,
    CompanyRegistrationRequest,
    LoginRequest,
)
from app.utils.jwt_utils import get_current_user_id

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/v1/auth",
)


@auth_bp.post("/register/student")
def register_student():
    data = request.get_json()

    registration_request = StudentRegistrationRequest.model_validate(data)

    response = auth_service.register_student(registration_request)

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.CREATED,
    )


@auth_bp.post("/register/company")
def register_company():
    data = request.get_json()
    registration_request = CompanyRegistrationRequest.model_validate(data)
    response = auth_service.register_company(registration_request)
    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.CREATED,
    )


@auth_bp.post("/login")
def login():
    data = request.get_json()
    login_request = LoginRequest.model_validate(data)
    response = auth_service.login(login_request)

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@auth_bp.get("/me")
@authenticated_required
def get_current_user():
    user_id = get_current_user_id()

    response = auth_service.get_current_user(user_id)

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )