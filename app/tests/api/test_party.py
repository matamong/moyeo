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
    data = {"name": "Foo", "nickname": "matamong"}
    response = client.post(f"{settings.API_V1_STR}/party", headers=normal_user_token_headers, json=data)
    content = response.json()
    print(content)

    assert response.status_code == 200
    assert content["name"] == data["name"]
    assert "id" in content
    assert "leader_id" in content
    assert "is_private" in content
    assert "code" in content
    assert "access_code" in content
    assert "created_at" in content


# TODO Super User only or leader(?) and just change is_active field
def test_delete_my_party():
    pass


def test_join_party():
    pass


def test_withdraw_party():
    pass

