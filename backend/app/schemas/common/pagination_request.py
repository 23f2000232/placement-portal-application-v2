from pydantic import BaseModel, ConfigDict, Field


class PaginationRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    page: int = Field(
        default=1,
        ge=1,
    )

    size: int = Field(
        default=20,
        ge=1,
        le=100,
    )