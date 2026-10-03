from app.gateway.rate_limit_service import RateLimitService


def test_service_uses_rule_engine_and_factory():
    rules = {
        "alice": {
            "algorithm": "fixed_window",
            "limit": 2,
            "window_seconds": 60,
        }
    }

    service = RateLimitService(
        rules=rules,
    )

    assert service.is_allowed("alice") is True
    assert service.is_allowed("alice") is True
    assert service.is_allowed("alice") is False


def test_service_supports_different_limits_for_different_clients():
    rules = {
        "alice_config_test": {
            "algorithm": "fixed_window",
            "limit": 2,
            "window_seconds": 60,
        },
        "bob_config_test": {
            "algorithm": "token_bucket",
            "capacity": 4,
            "refill_rate": 2,
        },
    }

    service = RateLimitService(
        rules=rules,
    )

    # Alice has a limit of 2
    assert service.is_allowed("alice_config_test") is True
    assert service.is_allowed("alice_config_test") is True
    assert service.is_allowed("alice_config_test") is False

    # Bob has a separate limit of 4
    assert service.is_allowed("bob_config_test") is True
    assert service.is_allowed("bob_config_test") is True
    assert service.is_allowed("bob_config_test") is True
    assert service.is_allowed("bob_config_test") is True
    assert service.is_allowed("bob_config_test") is False