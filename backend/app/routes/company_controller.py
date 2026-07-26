from http import HTTPStatus

from flask import Blueprint, jsonify, request

from app.dependencies import placement_drive_service
from app.schemas.requests.create_placement_drive_request import (
    CreatePlacementDriveRequest,
)
from app.utils.jwt_utils import get_current_user_id

company_bp = Blueprint(
    "company",
    __name__,
    url_prefix="/api/v1/company",
)


@company_bp.post("/drives")
def create_drive():
    company_user_id = get_current_user_id()

    data = request.get_json()

    create_request = CreatePlacementDriveRequest.model_validate(
        data,
    )

    response = placement_drive_service.create_drive(
        company_user_id=company_user_id,
        request=create_request,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.CREATED,
    )