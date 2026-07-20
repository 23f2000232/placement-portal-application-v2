from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentRegistrationRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    roll_number: str = Field(
        min_length=2,
        max_length=30,
    )

    phone_number: str = Field(
        min_length=10,
        max_length=15,
    )

    branch: str = Field(
        min_length=2,
        max_length=50,
    )

    semester: int = Field(
        ge=1,
        le=8,
    )

    cgpa: float = Field(
        ge=0,
        le=10,
    )