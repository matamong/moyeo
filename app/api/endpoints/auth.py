from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.api import dependency
from app.core.config import settings
from app.core.security import get_access_token, get_user_info, create_access_token, create_refresh_token, AUTH_BASE_URL
from app.schemas import AccessTokenResponse, UserInfoResponse, UserCreate
from app import crud, models

router = APIRouter()

# TODO nickname 중복 처리 handling
@router.get("/google/callback")
def google_auth(
        code: str,
        error: str = None,
        db: Session = Depends(dependency.get_db)
):
    """
    Handle the redirect from the Google OAuth2 API
    """

    if error:
        raise HTTPException(status_code=400, detail=error)
    token_response = get_access_token(code)
    token_response_model = AccessTokenResponse(**token_response)

    user_info = get_user_info(token_response_model.access_token)
    user_info_model = UserInfoResponse(**user_info)

    user = crud.user.get_by_email(db, email=user_info_model.email)

    if not user:
        user_in = UserCreate(
            email=user_info_model.email,
            nickname=user_info_model.name,
        )
        user = crud.user.create(db, obj_in=user_in)

    access_token = create_access_token(subject=str(user.id), email=user.email, nickname=user.nickname)
    refresh_token = create_refresh_token(subject=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.get("/google/login")
def google_login(request: Request):
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
    print(auth_url)
    return RedirectResponse(auth_url)
