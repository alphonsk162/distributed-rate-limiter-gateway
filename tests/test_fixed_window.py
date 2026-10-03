from app.rate_limiter.fixed_window import FixedWindowRateLimiter
from app.redis_client import create_redis_client

def create_limiter(limit=3, window_seconds=10):
    redis_client = create_redis_client()

    return FixedWindowRateLimiter(
        redis_client=redis_client,
        limit=limit,
        window_seconds=window_seconds,
    )

def test_requests_within_limit_are_allowed():
    limiter = create_limiter()

    assert limiter.is_allowed("alice_test_1") is True
    assert limiter.is_allowed("alice_test_1") is True
    assert limiter.is_allowed("alice_test_1") is True


def test_request_over_limit_is_rejected():
    limiter = create_limiter()

    assert limiter.is_allowed("alice_test_2") is True
    assert limiter.is_allowed("alice_test_2") is True
    assert limiter.is_allowed("alice_test_2") is True
    assert limiter.is_allowed("alice_test_2") is False


def test_clients_have_independent_limits():
    limiter = create_limiter()

    assert limiter.is_allowed("alice_test_3") is True
    assert limiter.is_allowed("alice_test_3") is True
    assert limiter.is_allowed("alice_test_3") is True
    assert limiter.is_allowed("alice_test_3") is False

    assert limiter.is_allowed("bob_test_3") is True