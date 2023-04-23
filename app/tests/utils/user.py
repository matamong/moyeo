from sqlalchemy.orm import Session

from app import crud
from app.models import User
from app.schemas import UserCreate
from app.tests.utils.utils import random_lower_string, random_email


def create_random_user(db: Session) -> User:
    nickname = random_lower_string()
    email = random_email()
    user_in = UserCreate(nickname=nickname, email=email)
    user = crud.user.create(db=db, obj_in=user_in)
    return user
