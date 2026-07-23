from uuid import UUID

from flask import Blueprint, jsonify, request

from app.dependencies import admin_service
from app.schemas.common.pagination_request import PaginationRequest
from app.schemas.requests import UserSearchRequest
from app.schemas.requests.user_filter_request import UserFilterRequest
from app.schemas.requests.user_sort_request import UserSortRequest

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


def pick(
    data: dict[str, str],
    *keys: str,
) -> dict[str, str]:
    return {key: data[key] for key in keys if key in data}