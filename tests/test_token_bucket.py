from app.rate_limiter.token_bucket import TokenBucketRateLimiter
from app.redis_client import create_redis_client
import time


def test_bucket_allows_burst_up_to_capacity():
    redis_client = create_redis_client()

    limiter = TokenBucketRateLimiter(
        redis_client=redis_client,
        capacity=3,
        refill_rate=1,
    )

    assert limiter.is_allowed("alice_token_test_1") is True
    assert limiter.is_allowed("alice_token_test_1") is True
    assert limiter.is_allowed("alice_token_test_1") is True

    assert limiter.is_allowed("alice_token_test_1") is False

    time.sleep(1)
    assert limiter.is_allowed("alice_token_test_1") is True
    assert limiter.is_allowed("alice_token_test_1") is False

    time.sleep(1)
    assert limiter.is_allowed("alice_token_test_1") is True
    assert limiter.is_allowed("alice_token_test_1") is False


def test_clients_have_independent_buckets():
    redis_client = create_redis_client()

    limiter = TokenBucketRateLimiter(
        redis_client=redis_client,
        capacity=2,
        refill_rate=1,
    )

    assert limiter.is_allowed("alice_token_test_2") is True
    assert limiter.is_allowed("alice_token_test_2") is True
    assert limiter.is_allowed("alice_token_test_2") is False

    assert limiter.is_allowed("bob_token_test_2") is True

