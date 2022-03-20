from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.link import create_random_link


def test_create_link(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"text": "http://Foo"}
    response = client.post(
        f"{settings.API_V1_STR}/links/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == data["text"]
    assert content["short_text"].find("http://") != -1
    assert "id" in content
    assert "owner_id" in content


def test_read_link(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    item = create_random_link(db)
    response = client.get(
        f"{settings.API_V1_STR}/links/{item.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == item.text
    assert content["short_text"] == item.short_text
    assert content["id"] == item.id
    assert content["owner_id"] == item.owner_id


def test_link_redirect(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"text": "http://ya.ru"}
    response = client.post(
        f"{settings.API_V1_STR}/links/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    print(content["short_text"])
    print(settings.API_V1_STR)
    response = client.get("/%s" % content["short_text"], allow_redirects=False)
    print("/%s" % content["short_text"])
    assert response.headers["location"] == "http://ya.ru"
    assert response.status_code == 307
