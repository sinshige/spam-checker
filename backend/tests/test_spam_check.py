from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_spam_check_flags_url() -> None:
    text = " ".join(f"https://example{i}.com" for i in range(10))
    response = client.post("/spam-check", json={"text": text})

    assert response.status_code == 200
    assert response.json() == {
        "is_spam": True,
        "score": 90,
        "reason": "URLを含むため",
    }


def test_spam_check_flags_ng_word() -> None:
    client.post("/spam-keywords", json={"keyword": "今すぐ"})
    client.post("/spam-keywords", json={"keyword": "クリック"})
    response = client.post("/spam-check", json={"text": "今すぐクリックしてください"})

    assert response.status_code == 200
    assert response.json() == {
        "is_spam": True,
        "score": 70,
        "reason": "NGワード「今すぐ、クリック」を含むため",
    }


def test_spam_check_accepts_normal_text() -> None:
    response = client.post(
        "/spam-check",
        json={"text": "今日は天気がよいので、公園を散歩しました。"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "is_spam": False,
        "score": 0,
        "reason": "該当するルールはありません",
    }


def test_spam_check_requires_text() -> None:
    response = client.post("/spam-check", json={})

    assert response.status_code == 422
