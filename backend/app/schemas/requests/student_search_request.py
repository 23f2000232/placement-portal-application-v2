from pydantic import BaseModel, ConfigDict, Field


class StudentSearchRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )