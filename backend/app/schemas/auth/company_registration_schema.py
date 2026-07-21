from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CompanyRegistrationRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    company_name: str = Field(
        min_length=2,
        max_length=100,
    )

    website: str | None = Field(
        default=None,
        min_length=5,
        max_length=500,
    )

    description: str = Field(
        min_length=10,
        max_length=1000,
    )

    industry: str = Field(
        min_length=2,
        max_length=100,
    )

    contact_person: str = Field(
        min_length=2,
        max_length=100,
    )

    contact_email: EmailStr

    contact_phone: str = Field(
        min_length=10,
        max_length=15,
    )