from functools import wraps

from flask_jwt_extended import verify_jwt_in_request

from app.enums import UserRole
from app.exceptions.common import ForbiddenException
from app.utils.jwt_utils import get_current_user_role


def role_required(
    required_role: UserRole,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            current_role = get_current_user_role()

            if current_role != required_role:
                raise ForbiddenException()

            return func(*args, **kwargs)

        return wrapper

    return decorator


def student_required(func):
    return role_required(
        UserRole.STUDENT,
    )(func)


def company_required(func):
    return role_required(
        UserRole.COMPANY,
    )(func)


def admin_required(func):
    return role_required(
        UserRole.ADMIN,
    )(func)


def authenticated_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return func(*args, **kwargs)

    return wrapper