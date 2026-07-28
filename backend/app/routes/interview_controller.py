from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.decorators.role_decorators import company_required, student_required
from app.dependencies import interview_service
from app.schemas.requests.company.complete_interview_request import (
    CompleteInterviewRequest,
)
from app.schemas.requests.company.create_interview_request import CreateInterviewRequest
from app.schemas.requests.company.update_interview_request import UpdateInterviewRequest
from app.utils.jwt_utils import get_current_user_id

interview_bp = Blueprint(
    "interview",
    __name__,
    url_prefix="/api/v1",
)


@interview_bp.post("/company/applications/<uuid:application_id>/interviews")
@jwt_required()
@company_required
def create_interview(
    application_id,
):
    data = request.get_json()

    create_request = CreateInterviewRequest.model_validate(
        data,
    )

    response = interview_service.create_interview(
        company_user_id=get_current_user_id(),
        application_id=application_id,
        request=create_request,
    )

    return (
        jsonify(
            response.model_dump(
                mode="json",
            )
        ),
        HTTPStatus.CREATED,
    )


@interview_bp.patch("/company/interviews/<uuid:interview_id>")
@jwt_required()
@company_required
def update_interview(
    interview_id,
):
    data = request.get_json()

    update_request = UpdateInterviewRequest.model_validate(
        data,
    )

    response = interview_service.update_interview(
        company_user_id=get_current_user_id(),
        interview_id=interview_id,
        request=update_request,
    )

    return (
        jsonify(
            response.model_dump(
                mode="json",
            )
        ),
        HTTPStatus.OK,
    )


@interview_bp.patch("/company/interviews/<uuid:interview_id>/complete")
@jwt_required()
@company_required
def complete_interview(
    interview_id,
):
    data = request.get_json()

    complete_request = CompleteInterviewRequest.model_validate(
        data,
    )

    response = interview_service.complete_interview(
        company_user_id=get_current_user_id(),
        interview_id=interview_id,
        request=complete_request,
    )

    return (
        jsonify(
            response.model_dump(
                mode="json",
            )
        ),
        HTTPStatus.OK,
    )


@interview_bp.get("/company/interviews/<uuid:interview_id>")
@jwt_required()
@company_required
def get_interview(
    interview_id,
):
    response = interview_service.get_interview(
        company_user_id=get_current_user_id(),
        interview_id=interview_id,
    )

    return (
        jsonify(
            response.model_dump(
                mode="json",
            )
        ),
        HTTPStatus.OK,
    )


@interview_bp.get("/company/applications/<uuid:application_id>/interviews")
@jwt_required()
@company_required
def get_application_interviews(
    application_id,
):
    response = interview_service.get_application_interviews(
        company_user_id=get_current_user_id(),
        application_id=application_id,
    )

    return (
        jsonify(
            [
                interview.model_dump(
                    mode="json",
                )
                for interview in response
            ]
        ),
        HTTPStatus.OK,
    )


@interview_bp.get("/student/interviews")
@jwt_required()
@student_required
def get_student_upcoming_interviews():

    response = interview_service.get_student_upcoming_interviews(
        student_user_id=get_current_user_id(),
    )

    return (
        jsonify(
            [
                interview.model_dump(
                    mode="json",
                )
                for interview in response
            ]
        ),
        HTTPStatus.OK,
    )


@interview_bp.get("/company/interviews")
@jwt_required()
@company_required
def get_company_upcoming_interviews():

    response = interview_service.get_company_upcoming_interviews(
        company_user_id=get_current_user_id(),
    )

    return (
        jsonify(
            [
                interview.model_dump(
                    mode="json",
                )
                for interview in response
            ]
        ),
        HTTPStatus.OK,
    )