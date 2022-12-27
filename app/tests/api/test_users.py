from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_V1_STR}/hello")
    content = response.json()


###
# TDD ing...
###
# def test_create_user(
#         client: TestClient, db: Session
# ) -> None:
#     data = {"email": "matamong@matamong.com", "nickname": "matamong_is_awsome"}
#     response = client.post(
#         f"{settings.API_V1_STR}/users/",
#         json=data,
#     )
#     assert response.status_code == 200
#     content = response.json()
#     assert content["email"] == data["email"]
#     assert content["nickname"] == data["email"]
#     assert "id" in content
