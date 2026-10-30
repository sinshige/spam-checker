from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_list_and_delete_spam_keyword() -> None:
    created = client.post("/spam-keywords", json={"keyword": "限定"})

    assert created.status_code == 201
    item = created.json()
    assert item["keyword"] == "限定"
    assert item["is_active"] is True

    listed = client.get("/spam-keywords")

    assert listed.status_code == 200
    assert [keyword["id"] for keyword in listed.json()] == [item["id"]]

    deleted = client.delete(f"/spam-keywords/{item['id']}")

    assert deleted.status_code == 204
    assert client.get("/spam-keywords").json() == []


def test_spam_check_uses_only_active_database_keywords() -> None:
    active = client.post("/spam-keywords", json={"keyword": "現金プレゼント"})
    inactive = client.post(
        "/spam-keywords",
        json={"keyword": "確実に無視", "is_active": False},
    )
    assert active.status_code == 201
    assert inactive.status_code == 201

    response = client.post(
        "/spam-check",
        json={"text": "現金プレゼントと確実に無視"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "is_spam": True,
        "score": 70,
        "reason": "NGワード「現金プレゼント」を含むため",
    }


def test_delete_missing_keyword_returns_404() -> None:
    response = client.delete("/spam-keywords/999")

    assert response.status_code == 404
