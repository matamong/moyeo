from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.security import create_access_token, create_refresh_token
from app.models import User
from app.schemas import UserCreate
from app.tests.utils.utils import random_lower_string, random_email


def create_random_user(db: Session) -> User:
    nickname = random_lower_string()
    email = random_email()
    user_in = UserCreate(nickname=nickname, email=email)
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def user_authentication_headers(*, client: TestClient, user: User) -> Dict[str, str]:
    access_token = create_access_token(subject=str(user.id), email=user.email, nickname=user.nickname)
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


def authentication_token_from_email(*, db: Session, client: TestClient, email: str) -> Dict[str, str]:
    """
    Return a valid token for the user with given email,
    If the user doesn't exist it is created first.
    """
    user = crud.user.get_by_email(db=db, email=email)
    if not user:
        nickname = random_lower_string()
        user_in = UserCreate(nickname=nickname, email=email)
        user = crud.user.create(db=db, obj_in=user_in)
    return user_authentication_headers(client=client, user=user)
