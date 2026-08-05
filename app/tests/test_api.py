from app.tests.conftest import client


def test_health():

    response = client.get("/api/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_invalid_url():

    response = client.post(
        "/api/audit",
        json={
            "url": "invalid-url"
        }
    )

    assert response.status_code == 422