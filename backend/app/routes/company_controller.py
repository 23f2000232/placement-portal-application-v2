from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, jsonify, request

from app.decorators.role_decorators import company_required
from app.dependencies import placement_drive_service, company_service
from app.schemas.common.pagination_request import PaginationRequest
from app.schemas.requests.company.company_application_filter_request import (
    CompanyApplicationFilterRequest,
)
from app.schemas.requests.company.company_application_search_request import (
    CompanyApplicationSearchRequest,
)
from app.schemas.requests.company.company_application_sort_request import (
    CompanyApplicationSortRequest,
)
from app.schemas.requests.placement.create_placement_drive_request import (
    CreatePlacementDriveRequest,
)
from app.schemas.requests.placement.placement_drive_filter_request import (
    PlacementDriveFilterRequest,
)
from app.schemas.requests.placement.placement_drive_search_request import (
    PlacementDriveSearchRequest,
)
from app.schemas.requests.placement.placement_drive_sort_request import (
    PlacementDriveSortRequest,
)
from app.schemas.requests.placement.update_placement_drive_request import (
    UpdatePlacementDriveRequest,
)
from app.utils.jwt_utils import get_current_user_id

company_bp = Blueprint(
    "company",
    __name__,
    url_prefix="/api/v1/company",
)


@company_bp.post("/drives")
@company_required
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


@company_bp.put("/drives/<uuid:drive_id>")
@company_required
def update_drive(drive_id: UUID):
    company_user_id = get_current_user_id()

    request_body = UpdatePlacementDriveRequest.model_validate(
        request.get_json(),
    )

    response = placement_drive_service.update_drive(
        company_user_id=company_user_id,
        drive_id=drive_id,
        request=request_body,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.patch("/drives/<uuid:drive_id>/open")
@company_required
def open_drive(drive_id: UUID):
    company_user_id = get_current_user_id()

    response = placement_drive_service.open_drive(
        company_user_id=company_user_id,
        drive_id=drive_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.patch("/drives/<uuid:drive_id>/close")
@company_required
def close_drive(drive_id: UUID):
    company_user_id = get_current_user_id()

    response = placement_drive_service.close_drive(
        company_user_id=company_user_id,
        drive_id=drive_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.patch("/drives/<uuid:drive_id>/cancel")
@company_required
def cancel_drive(drive_id: UUID):
    company_user_id = get_current_user_id()

    response = placement_drive_service.cancel_drive(
        company_user_id=company_user_id,
        drive_id=drive_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.delete("/drives/<uuid:drive_id>")
@company_required
def delete_drive(drive_id: UUID):
    company_user_id = get_current_user_id()

    placement_drive_service.delete_drive(
        company_user_id=company_user_id,
        drive_id=drive_id,
    )

    return (
        "",
        HTTPStatus.NO_CONTENT,
    )


@company_bp.get("/drives")
@company_required
def get_company_drives():
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

    filters = PlacementDriveFilterRequest.model_validate(
        {
            key: args[key]
            for key in (
                "status",
                "job_type",
                "is_remote",
            )
            if key in args
        }
    )

    sorting = PlacementDriveSortRequest.model_validate(
        {
            key: args[key]
            for key in (
                "sort_by",
                "sort_direction",
            )
            if key in args
        }
    )

    search = PlacementDriveSearchRequest.model_validate(
        {key: args[key] for key in ("search",) if key in args}
    )

    company_user_id = get_current_user_id()

    response = placement_drive_service.get_company_drives(
        company_user_id=company_user_id,
        pagination=pagination,
        filters=filters,
        sorting=sorting,
        search=search,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.get("/drives/<uuid:drive_id>/applications")
@company_required
def get_drive_applications(
    drive_id: UUID,
):
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

    filters = CompanyApplicationFilterRequest.model_validate(
        {key: args[key] for key in ("status",) if key in args}
    )

    sorting = CompanyApplicationSortRequest.model_validate(
        {
            key: args[key]
            for key in (
                "sort_by",
                "sort_direction",
            )
            if key in args
        }
    )

    search = CompanyApplicationSearchRequest.model_validate(
        {key: args[key] for key in ("search",) if key in args}
    )

    company_user_id = get_current_user_id()

    response = company_service.get_drive_applications(
        company_user_id=company_user_id,
        drive_id=drive_id,
        pagination=pagination,
        filters=filters,
        sorting=sorting,
        search=search,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.get("/applications/<uuid:application_id>")
@company_required
def get_application(
    application_id: UUID,
):
    company_user_id = get_current_user_id()

    response = company_service.get_application(
        company_user_id=company_user_id,
        application_id=application_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.patch("/applications/<uuid:application_id>/under-review")
@company_required
def mark_under_review(
    application_id: UUID,
):
    company_user_id = get_current_user_id()

    response = company_service.mark_under_review(
        company_user_id=company_user_id,
        application_id=application_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.patch("/applications/<uuid:application_id>/shortlist")
@company_required
def shortlist_application(
    application_id: UUID,
):
    company_user_id = get_current_user_id()

    response = company_service.shortlist_application(
        company_user_id=company_user_id,
        application_id=application_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.patch("/applications/<uuid:application_id>/schedule-interview")
@company_required
def schedule_interview(
    application_id: UUID,
):
    company_user_id = get_current_user_id()

    response = company_service.schedule_interview(
        company_user_id=company_user_id,
        application_id=application_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.patch("/applications/<uuid:application_id>/select")
@company_required
def select_application(
    application_id: UUID,
):
    company_user_id = get_current_user_id()

    response = company_service.select_application(
        company_user_id=company_user_id,
        application_id=application_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )


@company_bp.patch("/applications/<uuid:application_id>/reject")
@company_required
def reject_application(
    application_id: UUID,
):
    company_user_id = get_current_user_id()

    response = company_service.reject_application(
        company_user_id=company_user_id,
        application_id=application_id,
    )

    return (
        jsonify(response.model_dump(mode="json")),
        HTTPStatus.OK,
    )