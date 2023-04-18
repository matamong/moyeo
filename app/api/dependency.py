from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from app import models, schemas, crud
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal


bearer = HTTPBearer()


def get_db() -> Generator:
    print("db")
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# TODO 굳이 DB접근해서 user 객체 받아야하능가...
def get_current_user(
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(bearer)
) -> models.User:
    if credentials is None:
        raise HTTPException(status_code=400, detail="Not authenticated")
    try:
        payload = jwt.decode(
            credentials.credentials, settings.SECRET_KEY, algorithms=security.ALGORITHM
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as e:
        print(e)   # TODO: erase
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
