from pydantic import BaseModel, ConfigDict, Field


class UpdateStudentProfileRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    full_name: str = Field(min_length=2, max_length=100)
    phone_number: str = Field(min_length=10, max_length=15)
    branch: str = Field(min_length=2, max_length=50)
    semester: int = Field(ge=1, le=8)
    cgpa: float = Field(ge=0, le=10)
    current_backlogs: int = Field(ge=0)
    skills: list[str] = Field(default_factory=list, max_length=30)
