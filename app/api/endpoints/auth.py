from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse

from app.core.config import settings
from app.core.security import get_access_token, get_user_info, create_access_token, create_refresh_token, AUTH_BASE_URL
from app.schemas import AccessTokenResponse, UserInfoResponse

router = APIRouter()


@router.get("/google/callback")
def google_auth(code: str, error: str = None):
    """
    Handle the redirect from the Google OAuth2 API
    """

    if error:
        raise HTTPException(status_code=400, detail=error)
    token_response = get_access_token(code)
    token_response_model = AccessTokenResponse(**token_response)

    user_info = get_user_info(token_response_model.access_token)
    user_info_model = UserInfoResponse(**user_info)


    ###
    # User save function is here.
    ###
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
    return RedirectResponse(auth_url)
