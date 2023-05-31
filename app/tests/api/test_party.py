from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.core.config import settings
from app.tests.utils.party import create_random_party_with_user, create_random_party_with_random_user, \
    create_random_party_user
from app.tests.utils.user import create_random_user, authentication_token_from_email
from app.tests.utils.utils import random_lower_string


# TODO Super User only
def read_parties():
    pass


def test_get_my_parties(db: Session, client: TestClient) -> None:
    user = create_random_user(db=db)
    headers = authentication_token_from_email(db=db, client=client, email=user.email)

    response = client.get(f"{settings.API_V1_STR}/party/me", headers=headers)
    content = response.json()

    assert len(content) == 0
    assert response.status_code == 200

    party_nickname1 = random_lower_string()
    party = create_random_party_with_user(db=db, user=user, party_nickname=party_nickname1)
    response2 = client.get(f"{settings.API_V1_STR}/party/me", headers=headers)
    content2 = response2.json()

    assert response2.status_code == 200
    assert len(content2) == 1
    assert content2[0]["id"] == party.id
    assert content2[0]["name"] == party.name
    assert content2[0]["desc"] == party.desc
    assert content2[0]["img_path"] == party.img_path
    assert content2[0]["leader_id"] == party.leader_id
    assert "code" not in content2[0]
    assert "access_code" not in content2[0]
    assert content2[0]["is_private"] is not None
    assert content2[0]["created_at"] is not None

    party_nickname2 = random_lower_string()
    party2 = create_random_party_with_user(db=db, user=user, party_nickname=party_nickname2)
    response3 = client.get(f"{settings.API_V1_STR}/party/me", headers=headers)
    content3 = response3.json()

    assert response3.status_code == 200
    assert len(content3) == 2
    assert content3[1]["id"] == party2.id
    assert content3[1]["name"] == party2.name
    assert content3[1]["desc"] == party2.desc
    assert content3[1]["img_path"] == party2.img_path
    assert content3[1]["leader_id"] == party2.leader_id
    assert "code" not in content3[1]
    assert "access_code" not in content3[1]
    assert content3[1]["is_private"] is not None
    assert content3[1]["created_at"] is not None


def test_get_party_by_id(db: Session, client: TestClient) -> None:
    party = create_random_party_with_random_user(db=db)
    response = client.get(f"{settings.API_V1_STR}/party/{party.id}")
    content = response.json()

    assert response.status_code == 200
    assert content["id"] == party.id
    assert content["name"] == party.name
    assert content["desc"] == party.desc
    assert content["img_path"] == party.img_path
    assert "code" not in content
    assert "access_code" not in content
    assert content["is_private"] is not None
    assert content["created_at"] is not None


def test_get_party_with_users(db: Session, client: TestClient) -> None:
    leader = create_random_user(db=db)
    leader_party_nickname = random_lower_string()
    party = create_random_party_with_user(db=db, user=leader, party_nickname=leader_party_nickname)
    party_user = create_random_party_user(db=db, party_id=party.id)
    response = client.get(f"{settings.API_V1_STR}/party/party-with-users/{party.id}")
    content = response.json()

    assert response.status_code == 200
    assert content["id"] == party.id
    assert content["name"] == party.name
    assert content["desc"] == party.desc
    assert content["leader_id"] == leader.id
    assert content["img_path"] == party.img_path
    assert "code" not in content
    assert "access_code" not in content
    assert content["is_private"] is not None
    assert content["created_at"] is not None

    assert len(content["party_user_set"]) == 2
    assert content["party_user_set"][0]["nickname"] == leader_party_nickname
    assert content["party_user_set"][0]["is_manager"] is True
    assert content["party_user_set"][1]["id"] == party_user.id
    assert content["party_user_set"][1]["nickname"] == party_user.nickname
    assert content["party_user_set"][1]["is_manager"] is False


def test_get_party_by_code(db: Session, client: TestClient) -> None:
    party = create_random_party_with_random_user(db=db)
    response = client.get(f"{settings.API_V1_STR}/party/code/{party.code}")
    content = response.json()

    assert response.status_code == 200
    assert content["id"] == party.id
    assert content["name"] == party.name
    assert content["desc"] == party.desc
    assert content["img_path"] == party.img_path
    assert "code" not in content
    assert "access_code" not in content
    assert content["is_private"] is not None
    assert content["created_at"] is not None


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
    assert "code" not in content
    assert "access_code" not in content
    assert "created_at" in content


# TODO Super User only or leader(?) and just change is_active field
def test_delete_my_party():
    pass


"""
# Party User
"""


# TODO
def test_get_party_user(db: Session, client: TestClient) -> None:
    pass


def test_join_party(db: Session, client: TestClient) -> None:
    party = create_random_party_with_random_user(db=db)
    user = create_random_user(db=db)
    headers = authentication_token_from_email(db=db, client=client, email=user.email)
    nickname = random_lower_string()
    data = {"party_id": party.id, "nickname": nickname}
    response = client.post(f"{settings.API_V1_STR}/party/join", headers=headers, json=data)
    content = response.json()

    assert response.status_code == 200
    assert "id" in content
    assert content["party_id"] == party.id
    assert content["is_manager"] is False
    assert content["nickname"] == nickname


def test_withdraw_party_user(db: Session, client: TestClient) -> None:
    party = create_random_party_with_random_user(db=db)
    user = create_random_user(db=db)
    party_user = create_random_party_user(db=db, party_id=party.id, user=user)

    headers = authentication_token_from_email(db=db, client=client, email=user.email)
    response = client.delete(f"{settings.API_V1_STR}/party/withdraw/{party.id}", headers=headers)
    content = response.json()
    assert response.status_code == 200
    assert content["id"] == party_user.id
    assert content["party_id"] == party.id
    assert content["is_manager"] is False
    assert content["nickname"] == party_user.nickname


# TODO
def test_withdraw_party_if_only_user_is_leader(db: Session, client: TestClient) -> None:
    pass

