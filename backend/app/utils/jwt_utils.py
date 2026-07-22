from uuid import UUID

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
)

from app.enums import UserRole
from app.models import User


def create_access_token_for_user(user: User | None) -> str:
    return create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role.value,
        },
    )


def get_current_user_id() -> UUID:
    return UUID(get_jwt_identity())


def get_current_user_role() -> UserRole:
    claims = get_jwt()
    return UserRole(claims["role"])