from pydantic import BaseModel, ConfigDict


class RefreshTokenResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    access_token: str

    token_type: str

    expires_in: int