from unittest.mock import Mock

from app.rate_limiter.fixed_window import FixedWindowRateLimiter


def test_fixed_window_uses_atomic_redis_script():
    redis_client = Mock()
    redis_client.eval.return_value = 1

    limiter = FixedWindowRateLimiter(
        redis_client=redis_client,
        limit=3,
        window_seconds=10,
    )

    result = limiter.is_allowed("alice")

    assert result is True

    redis_client.eval.assert_called_once()

    args, kwargs = redis_client.eval.call_args

    script = args[0]
    number_of_keys = args[1]
    key = args[2]
    window_seconds = args[3]

    assert number_of_keys == 1
    assert key.startswith("rate_limit:fixed:alice:")
    assert window_seconds == 10

    assert "INCR" in script
    assert "EXPIRE" in script