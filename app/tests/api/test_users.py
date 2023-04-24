from typing import Dict

from starlette.testclient import TestClient

from app.core.config import settings


def test_get_user_me(client: TestClient, normal_user_token_headers: Dict[str, str]) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()

    assert current_user
    assert current_user["is_active"] is True
    assert current_user["email"] == settings.TEST_USER_EMAIL
