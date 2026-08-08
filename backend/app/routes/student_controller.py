from http import HTTPStatus
from uuid import UUID

import re
from uuid import uuid4

from flask import Blueprint, abort, jsonify, request, send_from_directory

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
from app.schemas.requests.student.update_student_profile_request import UpdateStudentProfileRequest
from app.utils.jwt_utils import get_current_user_id
from app.config import Config
from app.celery_app import celery
from app.tasks.placement_tasks import export_student_applications

student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/api/v1/student",
)


@student_bp.put("/profile")
@student_required
def update_profile():
    response = student_service.update_profile(
        get_current_user_id(),
        UpdateStudentProfileRequest.model_validate(request.get_json()),
    )
    return jsonify(response.model_dump(mode="json")), HTTPStatus.OK


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


@student_bp.get("/applications/export")
@student_required
def export_application_history():
    """Queue a CSV export; the Celery worker creates it outside the request."""
    student_user_id = get_current_user_id()
    task_id = str(uuid4())
    # Assign the id before enqueueing so it can safely name the export file.
    export_student_applications.apply_async(
        args=[str(student_user_id), task_id],
        task_id=task_id,
    )
    return jsonify({"task_id": task_id, "message": "Your export is being prepared. You will be notified when it is ready."}), HTTPStatus.ACCEPTED


@student_bp.get("/applications/export/<task_id>/download")
@student_required
def download_application_history_export(task_id: str):
    if not re.fullmatch(r"[a-f0-9-]{36}", task_id):
        abort(404)
    student = student_service.student_repository.get_by_user_id(get_current_user_id())
    filename = f"{student.id}_{task_id}.csv"
    if not (Config.EXPORT_DIRECTORY / filename).is_file():
        abort(404)
    return send_from_directory(Config.EXPORT_DIRECTORY, filename, as_attachment=True)


@student_bp.get("/applications/export/<task_id>/status")
@student_required
def get_application_export_status(task_id: str):
    """Expose only the current student's export task state and download URL."""
    if not re.fullmatch(r"[a-f0-9-]{36}", task_id):
        abort(404)
    student = student_service.student_repository.get_by_user_id(get_current_user_id())
    filename = f"{student.id}_{task_id}.csv"
    destination = Config.EXPORT_DIRECTORY / filename
    task = celery.AsyncResult(task_id)
    if destination.is_file():
        return jsonify({
            "status": "SUCCESS",
            "download_url": f"/api/v1/student/applications/export/{task_id}/download",
        }), HTTPStatus.OK
    if task.state == "FAILURE":
        return jsonify({"status": "FAILURE", "message": "The export could not be created."}), HTTPStatus.OK
    return jsonify({"status": task.state}), HTTPStatus.OK


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
