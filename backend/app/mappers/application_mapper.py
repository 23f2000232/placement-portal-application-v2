from app.models import Application
from app.schemas.response.application.application_response import (
    ApplicationResponse,
)


class ApplicationMapper:

    @staticmethod
    def to_response(
        application: Application,
    ) -> ApplicationResponse:
        return ApplicationResponse(
            id=application.id,
            drive_id=application.placement_drive_id,
            status=application.status,
            applied_at=application.created_at,
        )