import datetime
from typing import Optional, List
from urllib.parse import urlencode

from jose import jwt
import httpx
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse

from app.core.config import settings

router = APIRouter()

ALGORITHM = "HS256"
AUTH_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"


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


def create_access_token(
        subject: str,
        expire_delta: Optional[datetime.timedelta] = None,
        **kwargs
):
    if expire_delta:
        expire = datetime.datetime.utcnow() + expire_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "exp": expire,
        "sub": subject,
        **kwargs
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(
        subject: str,
        expires_delta: Optional[datetime.timedelta] = None,
        **kwargs,
):
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(days=15)

    payload = {
        "exp": expire,
        "sub": subject,
        **kwargs
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def get_access_token(code: str):
    """
    Exchange the authorization code for an access token
    """
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = httpx.post("https://www.googleapis.com/oauth2/v4/token", data=params, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error exchanging code for token")
    return response.json()


def get_user_info(access_token: str):
    """Get the user's profile information from the Google API"""
    headers = {
        # "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}",
        # "Accept": "application/json"
    }
    # response = httpx.get("https://www.googleapis.com/oauth2/v4/token", headers=headers)
    response = httpx.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error getting user info")
    return response.json()


@router.get("/google/callback")
def google_auth(code: str, error: str = None):
    """
    Handle the redirect from the Google OAuth2 API
    """
    print('here')

    if error:
        raise HTTPException(status_code=400, detail=error)
    token_response = get_access_token(code)
    print(token_response)
    token_response_model = AccessTokenResponse(**token_response)

    user_info = get_user_info(token_response_model.access_token)
    print(user_info)
    user_info_model = UserInfoResponse(**user_info)

    print(user_info_model)

    # user = User.get(email=user_info_model.email)
    #
    # if not user:
    #     user = User(
    #         email=user_info_model.email,
    #         name=user_info_model.name,
    #     )
    #     user.save()
    # access_token = create_access_token(subject=user.id)
    # refresh_token = create_refresh_token(subject=user.id)
    access_token = create_access_token(subject=user_info_model.email, name="test")
    refresh_token = create_refresh_token(subject=user_info_model.email, name="test")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.get("/google/login")
def login(request: Request):
    """
    Initiate the OAuth2 authorization flow
    """
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI
    }
    auth_url = f"{AUTH_BASE_URL}?{urlencode(params)}"
    return RedirectResponse(auth_url)
