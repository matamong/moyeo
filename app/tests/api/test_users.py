from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import get_app_settings

APP_SETTINGS = get_app_settings()


def test(client: TestClient, db: Session) -> None:
    print(f"{APP_SETTINGS.api_prefix}/hello")
    response = client.get(f"{APP_SETTINGS.api_prefix}/hello")
    assert response.status_code == 200
    content = response.json()
    print(content)


def test_create_user(
        client: TestClient, db: Session
) -> None:
    data = {"email": "matamong@matamong.com", "nickname": "matamong_is_awsome"}
    response = client.post(
        f"{APP_SETTINGS.api_prefix}/users/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == data["email"]
    assert content["nickname"] == data["email"]
    assert "id" in content
