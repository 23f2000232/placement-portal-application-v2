from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, jsonify, request

from app.decorators.role_decorators import student_required
from app.dependencies import student_service
from app.schemas.common.pagination_request import PaginationRequest
from app.schemas.requests.student.student_application_filter_request import (
    StudentApplicationFilterRequest,
)
from app.schemas.requests.student.student_application_search_request import (
    StudentApplicationSearchRequest,
)
from app.schemas.requests.student.student_application_sort_request import (
    StudentApplicationSortRequest,
)
from app.schemas.requests.student.student_drive_filter_request import (
    StudentDriveFilterRequest,
)
from app.schemas.requests.student.student_drive_search_request import (
    StudentDriveSearchRequest,
)
from app.schemas.requests.student.student_drive_sort_request import (
    StudentDriveSortRequest,
)
from app.utils.jwt_utils import get_current_user_id

student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/api/v1/student",
)


@student_bp.get("/drives")
@student_required
def get_available_drives():
    args = request.args.to_dict(flat=True)

    pagination = PaginationRequest.model_validate(
        {
            key: args[key]
            for key in (
                "page",
                "size",
            )
            if key in args
        }
    )

    filters = StudentDriveFilterRequest.model_validate(
        {
            key: args[key]
            for key in (
                "job_type",
                "is_remote",
            )
            if key in args
        }
    )

    sorting = StudentDriveSortRequest.model_validate(
        {
            key: args[key]
            for key in (
                "sort_by",
                "sort_direction",
            )
            if key in args
        }
    )

    search = StudentDriveSearchRequest.model_validate(
        {key: args[key] for key in ("search",) if key in args}
    )

    student_user_id = get_current_user_id()

    response = student_service.get_available_drives(
        student_user_id=student_user_id,
        pagination=pagination,
        filters=filters,
        sorting=sorting,
        search=search,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@student_bp.get("/drives/<uuid:drive_id>")
@student_required
def get_available_drive(
    drive_id: UUID,
):
    student_user_id = get_current_user_id()

    response = student_service.get_available_drive(
        student_user_id=student_user_id,
        drive_id=drive_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@student_bp.post("/drives/<uuid:drive_id>/apply")
@student_required
def apply_to_drive(
    drive_id: UUID,
):
    student_user_id = get_current_user_id()

    response = student_service.apply_to_drive(
        student_user_id=student_user_id,
        drive_id=drive_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.CREATED,
    )


@student_bp.get("/applications")
@student_required
def get_my_applications():
    args = request.args.to_dict(flat=True)

    pagination = PaginationRequest.model_validate(
        {
            key: args[key]
            for key in (
                "page",
                "size",
            )
            if key in args
        }
    )

    filters = StudentApplicationFilterRequest.model_validate(
        {key: args[key] for key in ("status",) if key in args}
    )

    sorting = StudentApplicationSortRequest.model_validate(
        {
            key: args[key]
            for key in (
                "sort_by",
                "sort_direction",
            )
            if key in args
        }
    )

    search = StudentApplicationSearchRequest.model_validate(
        {key: args[key] for key in ("search",) if key in args}
    )

    student_user_id = get_current_user_id()

    response = student_service.get_my_applications(
        student_user_id=student_user_id,
        pagination=pagination,
        filters=filters,
        sorting=sorting,
        search=search,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@student_bp.delete("/applications/<uuid:application_id>")
@student_required
def withdraw_application(
    application_id: UUID,
):
    student_user_id = get_current_user_id()

    student_service.withdraw_application(
        student_user_id=student_user_id,
        application_id=application_id,
    )

    return "", HTTPStatus.NO_CONTENT


@student_bp.post("/resume")
@student_required
def upload_resume():
    student_user_id = get_current_user_id()

    file = request.files.get("resume")

    response = student_service.upload_resume(
        student_user_id=student_user_id,
        file=file,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.CREATED,
    )


@student_bp.get("/resume")
@student_required
def get_resume():
    student_user_id = get_current_user_id()

    response = student_service.get_resume(
        student_user_id=student_user_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@student_bp.delete("/resume")
@student_required
def delete_resume():
    student_user_id = get_current_user_id()

    student_service.delete_resume(
        student_user_id=student_user_id,
    )

    return (
        "",
        HTTPStatus.NO_CONTENT,
    )