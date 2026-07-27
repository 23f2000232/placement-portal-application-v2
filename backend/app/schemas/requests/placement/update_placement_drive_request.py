from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.enums import InterviewMode, JobType


class UpdatePlacementDriveRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
        extra="forbid",
    )

    title: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str = Field(
        min_length=20,
        max_length=5000,
    )

    job_location: str = Field(
        min_length=2,
        max_length=100,
    )

    is_remote: bool = False

    salary_package: Decimal = Field(
        gt=0,
    )

    minimum_cgpa: Decimal = Field(
        ge=0,
        le=10,
    )

    eligible_branches: list[str] = Field(
        min_length=1,
    )

    maximum_backlogs: int = Field(
        ge=0,
    )

    experience_required: int = Field(
        ge=0,
    )

    vacancies: int = Field(
        gt=0,
    )

    application_deadline: datetime

    interview_date: datetime | None = None

    job_type: JobType

    interview_mode: InterviewMode