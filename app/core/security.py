import datetime
from typing import Optional

from fastapi import HTTPException
from jose import jwt
import httpx

from app.core.config import settings


ALGORITHM = "HS256"
AUTH_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"


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


#######
# Google OAuth
#######

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
        "Authorization": f"Bearer {access_token}",
    }
    response = httpx.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error getting user info")
    return response.json()
