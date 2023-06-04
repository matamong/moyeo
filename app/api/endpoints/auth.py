from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request, Depends, Response
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.api import dependency
from app.core.config import settings
from app.core.security import get_access_token, get_user_info, create_access_token, create_refresh_token, AUTH_BASE_URL
from app import crud, schemas


router = APIRouter()


# TODO nickname 중복 처리 handling
@router.post("/google/callback")
def google_auth(
        code_in: schemas.GoogleCode,
        response: Response,
        request: Request,
        db: Session = Depends(dependency.get_db)
):
    """
    Handle the redirect from the Google OAuth2 API.
    Requests other than localhost:8000 requests are set in Cookie in HttpOnly method.
    """
    if code_in.error:
        raise HTTPException(status_code=400, detail=code_in.error)
    token_response = get_access_token(code_in.code)
    token_response_model = schemas.AccessTokenResponse(**token_response)
    user_info = get_user_info(token_response_model.access_token)
    user_info_model = schemas.UserInfoResponse(**user_info)
    user = crud.user.get_by_email(db, email=user_info_model.email)

    if not user:
        user_in = schemas.UserCreate(
            email=user_info_model.email,
            nickname=user_info_model.name,
        )
        user = crud.user.create(db, obj_in=user_in)

    access_token = create_access_token(subject=str(user.id), email=user.email, nickname=user.nickname)
    refresh_token = create_refresh_token(subject=str(user.id))

    if "localhost:8000" in request.headers.get("referer"):
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    else:
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        return {"user": schemas.User.from_orm(user)}


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


@router.delete("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
