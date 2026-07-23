from app.models import User
from app.schemas.response.admin.user_summary_response import UserSummaryResponse


class UserMapper:

    @staticmethod
    def to_summary_response(
        user: User,
    ) -> UserSummaryResponse:
        return UserSummaryResponse(
            id=user.id,
            email=user.email,
            role=user.role,
            account_status=user.account_status,
            is_active=user.is_active,
        )