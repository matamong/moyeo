from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None
    scope: str


class UserInfoResponse(BaseModel):
    id: str
    name: str
    given_name: str
    family_name: str
    picture: str
    email: str
    verified_email: bool
    locale: str