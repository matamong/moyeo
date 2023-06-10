from typing import Optional

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
    given_name: Optional[str] = ''
    family_name: Optional[str] = ''
    picture: Optional[str] = ''
    email: Optional[str] = ''
    verified_email: bool
    locale: Optional[str] = ''


class GoogleCode(BaseModel):
    code: str
    error: str | None
