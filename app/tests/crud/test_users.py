from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas import UserCreate, UserUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_email


def test_create_user(db: Session) -> None:
    email = random_email()
    nickname = random_lower_string()
    user_in = UserCreate(email=email, nickname=nickname)
    user = crud.user.create(db=db, obj_in=user_in)

    assert user.email == email
    assert user.nickname == nickname


def test_get_user(db: Session) -> None:
    user = create_random_user(db=db)

    db_obj = crud.user.get(db=db, id=user.id)

    assert db_obj.id == user.id
    assert db_obj.email == user.email
    assert db_obj.nickname == user.nickname
    assert db_obj.is_active == user.is_active
    assert db_obj.updated_at == user.updated_at
    assert db_obj.created_at == user.created_at


def test_get_user_by_email(db: Session) -> None:
    user = create_random_user(db=db)

    db_obj = crud.user.get_by_email(db=db, email=user.email)

    assert db_obj.id == user.id
    assert db_obj.email == user.email
    assert db_obj.nickname == user.nickname
    assert db_obj.is_active == user.is_active
    assert db_obj.updated_at == user.updated_at
    assert db_obj.created_at == user.created_at


def test_get_user_by_email(db: Session) -> None:
    user = create_random_user(db=db)

    db_obj = crud.user.get_by_email(db=db, email=user.email)

    assert db_obj.id == user.id
    assert db_obj.email == user.email
    assert db_obj.nickname == user.nickname
    assert db_obj.is_active == user.is_active
    assert db_obj.updated_at == user.updated_at
    assert db_obj.created_at == user.created_at


def test_update_user(db: Session) -> None:
    user = create_random_user(db=db)

    updated_nickname = random_lower_string()
    user_in = UserUpdate(nickname=updated_nickname)
    updated_user = crud.user.update(db=db, db_obj=user, obj_in=user_in)

    assert updated_user.id == user.id
    assert updated_user.email == user.email
    assert updated_user.nickname == updated_nickname


def test_delete_user(db: Session) -> None:
    user = create_random_user(db=db)

    user2 = crud.user.remove(db=db, id=user.id)
    user3 = crud.user.get(db=db, id=user.id)

    assert user3 is None
    assert user2.id == user.id
    assert user2.email == user.email
    assert user2.nickname == user.nickname


# def test_google_login(client: TestClient) -> None:
#     url = "/api/v1/auth/google/login"
#     response = client.get(url)
#     print(response.content)
#     for k, v in response.headers.items():
#         print(f"{k} : {v}")
#
#     assert response.status_code == 302
#     assert response.headers["location"].startswith("https://accounts.google.com/o/oauth2")
#
#     redirect_uri = response.headers["location"].split("redirect_uri=")[1].split("&")[0]
#     parsed_redirect_uri = urlparse(redirect_uri)
#
#     callback_url = "http://localhost:8000" + parsed_redirect_uri
#     print(callback_url)
