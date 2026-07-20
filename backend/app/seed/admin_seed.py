import logging

from app.config import Config
from app.enums import UserRole
from app.extensions import db
from app.models import User

logger = logging.getLogger(__name__)


def seed_admin() -> None:
    admin = User.query.filter_by(role=UserRole.ADMIN).first()

    if admin:
        logger.info("Admin already exists.")
        return

    admin = User(role=UserRole.ADMIN)
    admin.set_email(Config.ADMIN_EMAIL)
    admin.set_password(Config.ADMIN_PASSWORD)

    db.session.add(admin)
    db.session.commit()

    logger.info("Admin account created successfully.")