from uuid import UUID

from flask import Blueprint, jsonify, request

from app.decorators.role_decorators import admin_required
from app.dependencies import admin_service
from app.schemas.common.pagination_request import PaginationRequest
from app.schemas.requests import (
    UserSearchRequest,
    StudentSearchRequest,
    StudentSortRequest,
    StudentFilterRequest,
)
from app.schemas.requests.company_filter_request import CompanyFilterRequest
from app.schemas.requests.company_search_request import CompanySearchRequest
from app.schemas.requests.company_sort_request import CompanySortRequest
from app.schemas.requests.user_filter_request import UserFilterRequest
from app.schemas.requests.user_sort_request import UserSortRequest
from app.utils.request_parser import pick
from app.enums import AccountStatus
from app.mappers.placement_drive_mapper import PlacementDriveMapper
from app.schemas.requests.placement.placement_drive_filter_request import PlacementDriveFilterRequest
from app.schemas.requests.placement.placement_drive_search_request import PlacementDriveSearchRequest
from app.schemas.requests.placement.placement_drive_sort_request import PlacementDriveSortRequest

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/v1/admin",
)

from http import HTTPStatus


@admin_bp.get("/dashboard")
@admin_required
def get_dashboard():
    return jsonify(admin_service.get_dashboard()), HTTPStatus.OK


@admin_bp.get("/drives/pending")
@admin_required
def get_pending_drives():
    drives = admin_service.get_pending_drives()
    return jsonify([PlacementDriveMapper.to_summary_response(drive).model_dump(mode="json") for drive in drives]), HTTPStatus.OK


@admin_bp.patch("/drives/<uuid:drive_id>/approve")
@admin_required
def approve_drive(drive_id: UUID):
    drive = admin_service.approve_drive(drive_id)
    return jsonify(PlacementDriveMapper.to_response(drive).model_dump(mode="json")), HTTPStatus.OK


@admin_bp.patch("/drives/<uuid:drive_id>/reject")
@admin_required
def reject_drive(drive_id: UUID):
    drive = admin_service.reject_drive(drive_id)
    return jsonify(PlacementDriveMapper.to_response(drive).model_dump(mode="json")), HTTPStatus.OK


@admin_bp.patch("/drives/<uuid:drive_id>/close")
@admin_required
def close_drive(drive_id: UUID):
    drive = admin_service.close_drive(drive_id)
    return jsonify(PlacementDriveMapper.to_response(drive).model_dump(mode="json")), HTTPStatus.OK


@admin_bp.patch("/drives/<uuid:drive_id>/cancel")
@admin_required
def cancel_drive(drive_id: UUID):
    drive = admin_service.cancel_drive(drive_id)
    return jsonify(PlacementDriveMapper.to_response(drive).model_dump(mode="json")), HTTPStatus.OK


@admin_bp.patch("/users/<uuid:user_id>/account-status")
@admin_required
def set_user_account_status(user_id: UUID):
    status = AccountStatus(request.get_json()["account_status"])
    response = admin_service.set_user_account_status(user_id, status)
    return jsonify(response.model_dump(mode="json")), HTTPStatus.OK


@admin_bp.get("/students/pending")
@admin_required
def get_pending_students():
    response = admin_service.get_pending_students()

    return (
        jsonify([student.model_dump(mode="json") for student in response]),
        HTTPStatus.OK,
    )


@admin_bp.patch("/students/<uuid:student_id>/approve")
@admin_required
def approve_student(student_id):
    response = admin_service.approve_student(student_id)

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@admin_bp.patch("/students/<uuid:student_id>/reject")
@admin_required
def reject_student(student_id):
    response = admin_service.reject_student(student_id)

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@admin_bp.get("/companies/pending")
@admin_required
def get_pending_companies():
    response = admin_service.get_pending_companies()

    return jsonify([company.model_dump(mode="json") for company in response]), 200


@admin_bp.patch("/companies/<uuid:company_id>/approve")
@admin_required
def approve_company(company_id: UUID):
    response = admin_service.approve_company(company_id)

    return jsonify(response.model_dump(mode="json")), 200


@admin_bp.patch("/companies/<uuid:company_id>/reject")
@admin_required
def reject_company(company_id: UUID):
    response = admin_service.reject_company(company_id)

    return jsonify(response.model_dump(mode="json")), 200


@admin_bp.get("/users")
@admin_required
def get_users():
    args = request.args.to_dict(flat=True)

    pagination = PaginationRequest.model_validate(
        pick(args, "page", "size"),
    )

    filters = UserFilterRequest.model_validate(
        pick(
            args,
            "role",
            "account_status",
            "is_active",
        ),
    )

    sorting = UserSortRequest.model_validate(
        pick(
            args,
            "sort_by",
            "sort_direction",
        ),
    )

    search = UserSearchRequest.model_validate(
        pick(args, "search"),
    )

    response = admin_service.get_users(
        pagination=pagination,
        filters=filters,
        sorting=sorting,
        search=search,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@admin_bp.get("/students")
@admin_required
def get_students():
    args = request.args.to_dict(flat=True)

    pagination = PaginationRequest.model_validate(
        pick(args, "page", "size"),
    )

    filters = StudentFilterRequest.model_validate(
        pick(
            args,
            "approval_status",
            "branch",
            "semester",
        ),
    )

    sorting = StudentSortRequest.model_validate(
        pick(
            args,
            "sort_by",
            "sort_direction",
        ),
    )

    search = StudentSearchRequest.model_validate(
        pick(args, "search"),
    )

    response = admin_service.get_students(
        pagination=pagination,
        filters=filters,
        sorting=sorting,
        search=search,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@admin_bp.get("/companies")
@admin_required
def get_companies():
    args = request.args.to_dict(flat=True)

    pagination = PaginationRequest.model_validate(
        pick(args, "page", "size"),
    )

    filters = CompanyFilterRequest.model_validate(
        pick(
            args,
            "approval_status",
            "industry",
        ),
    )

    sorting = CompanySortRequest.model_validate(
        pick(
            args,
            "sort_by",
            "sort_direction",
        ),
    )

    search = CompanySearchRequest.model_validate(
        pick(args, "search"),
    )

    response = admin_service.get_companies(
        pagination=pagination,
        filters=filters,
        sorting=sorting,
        search=search,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@admin_bp.get("/drives")
@admin_required
def get_drives():
    args = request.args.to_dict(flat=True)
    pagination = PaginationRequest.model_validate(pick(args, "page", "size"))
    filters = PlacementDriveFilterRequest.model_validate(
        pick(args, "status", "job_type", "is_remote")
    )
    sorting = PlacementDriveSortRequest.model_validate(
        pick(args, "sort_by", "sort_direction")
    )
    search = PlacementDriveSearchRequest.model_validate(pick(args, "search"))
    response = admin_service.get_drives(pagination, filters, sorting, search)
    return jsonify(response.model_dump(mode="json")), HTTPStatus.OK
