from uuid import UUID

from flask import Blueprint, jsonify, request

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

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/v1/admin",
)

from http import HTTPStatus


@admin_bp.get("/students/pending")
def get_pending_students():
    response = admin_service.get_pending_students()

    return (
        jsonify([student.model_dump(mode="json") for student in response]),
        HTTPStatus.OK,
    )


@admin_bp.patch("/students/<uuid:student_id>/approve")
def approve_student(student_id):
    response = admin_service.approve_student(student_id)

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@admin_bp.patch("/students/<uuid:student_id>/reject")
def reject_student(student_id):
    response = admin_service.reject_student(student_id)

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@admin_bp.get("/companies/pending")
def get_pending_companies():
    response = admin_service.get_pending_companies()

    return jsonify([company.model_dump(mode="json") for company in response]), 200


@admin_bp.patch("/companies/<uuid:company_id>/approve")
def approve_company(company_id: UUID):
    response = admin_service.approve_company(company_id)

    return jsonify(response.model_dump(mode="json")), 200


@admin_bp.patch("/companies/<uuid:company_id>/reject")
def reject_company(company_id: UUID):
    response = admin_service.reject_company(company_id)

    return jsonify(response.model_dump(mode="json")), 200


@admin_bp.get("/users")
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