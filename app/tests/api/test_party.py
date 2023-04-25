from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.core.config import settings


# TODO Super User only
def read_parties():
    pass


def test_get_my_parties(client: TestClient, normal_user_token_headers: Dict[str, str]) -> None:
    r = client.get(f"{settings.API_V1_STR}/party/me", headers=normal_user_token_headers)
    pass


def test_get_party_by_id():
    pass


def test_get_party_with_users():
    pass


def test_get_party_by_code():
    pass


def test_create_party(db: Session, client: TestClient, normal_user_token_headers: Dict[str, str]) -> None:
    pass


# TODO Super User only or leader(?) and just change is_active field
def test_delete_my_party():
    pass


def test_join_party():
    pass


def test_withdraw_party():
    pass

