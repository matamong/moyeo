import datetime
from typing import Generator, Optional

from fastapi import Depends, HTTPException, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from app import models, schemas, crud
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.core.security import create_access_token, create_refresh_token

bearer = HTTPBearer(auto_error=False)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# TODO 굳이 DB접근해서 user 객체 받아야하능가...
def get_current_user(
        response: Response,
        db: Session = Depends(get_db),
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
        access_token: Optional[str] = Cookie(...),
        refresh_token: Optional[str] = Cookie(...),
) -> models.User:
    refresh_token_data = None

    if credentials:
        if credentials == 'null' or credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        token = credentials.credentials
    elif access_token:
        token = access_token
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=security.ALGORITHM
        )
        token_data = schemas.TokenPayload(**payload)
    except ExpiredSignatureError:
        if refresh_token:
            try:
                refresh_payload = jwt.decode(
                    refresh_token, settings.SECRET_KEY, algorithms=security.ALGORITHM
                )
                token_data = schemas.TokenPayload(**refresh_payload)

            except (jwt.JWTError, ValidationError):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = crud.user.get(db, id=token_data.sub)

    if refresh_token_data:
        access_token = create_access_token(subject=str(user.id), email=user.email, nickname=user.nickname)
        refresh_token = create_refresh_token(subject=str(user.id))

        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
