from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_endpoint_reports_loaded_faqs():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["faqs_loaded"] >= 80


def test_chat_endpoint_returns_expected_shape():
    response = client.post(
        "/api/chat",
        json={"message": "How do I open a bank account?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "Accounts"
    assert body["is_fallback"] is False
    assert isinstance(body["answer"], str)


def test_chat_rejects_empty_message():
    response = client.post("/api/chat", json={"message": ""})

    assert response.status_code == 422


def test_chat_rejects_oversized_context_message():
    response = client.post(
        "/api/chat",
        json={"message": "hello", "recent_messages": ["x" * 501]},
    )

    assert response.status_code == 422


def test_invalid_calculation_does_not_crash_api():
    response = client.post(
        "/api/chat",
        json={"message": "EMI for 300000 at 10% for 0 years"},
    )

    assert response.status_code == 200
    assert response.json()["is_fallback"] is True
