from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_api_allows_requests():
    response = client.get(
        "/api/data",
        headers={"X-Client-ID": "api_test_client"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Request successful"
    }

def test_api_rejects_requests_after_rate_limit():
    client_id = "api_rate_limit_test_client"

    # The current API configuration needs this client.
    from app.main import rate_limit_service

    rate_limit_service.rule_engine.rules[client_id] = {
        "algorithm": "fixed_window",
        "limit": 2,
        "window_seconds": 60,
    }

    # Clear previous Redis state for this test client.
    redis_client = rate_limit_service.redis

    for key in redis_client.scan_iter(
        match=f"rate_limit:*:{client_id}:*"
    ):
        redis_client.delete(key)

    response_1 = client.get(
        "/api/data",
        headers={"X-Client-ID": client_id},
    )

    response_2 = client.get(
        "/api/data",
        headers={"X-Client-ID": client_id},
    )

    response_3 = client.get(
        "/api/data",
        headers={"X-Client-ID": client_id},
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 429

    assert response_3.json() == {
        "detail": "Rate limit exceeded"
    }

def test_api_uses_default_rate_limit_for_unknown_client():
    client_id = "default_policy_test_client"

    from app.main import rate_limit_service

    redis_client = rate_limit_service.redis

    for key in redis_client.scan_iter(
        match=f"rate_limit:*:{client_id}:*"
    ):
        redis_client.delete(key)

    responses = [
        client.get(
            "/api/data",
            headers={"X-Client-ID": client_id},
        )
        for _ in range(4)
    ]

    assert responses[0].status_code == 200
    assert responses[1].status_code == 200
    assert responses[2].status_code == 200
    assert responses[3].status_code == 429