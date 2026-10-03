from concurrent.futures import ThreadPoolExecutor

from app.rate_limiter.token_bucket import TokenBucketRateLimiter
from app.redis_client import create_redis_client


def test_token_bucket_concurrency():

    redis_client = create_redis_client()

    client_id = "concurrency_test_client"

    # Make sure this test starts with a fresh bucket.
    redis_client.delete(
        f"rate_limit:bucket:{client_id}"
    )

    limiter = TokenBucketRateLimiter(
        redis_client=redis_client,
        capacity=12,
        refill_rate=0,
    )

    def make_request():
        return limiter.is_allowed(client_id)

    with ThreadPoolExecutor(max_workers=20) as executor:

        results = list(
            executor.map(
                lambda _: make_request(),
                range(20),
            )
        )

    allowed = sum(results)
    rejected = len(results) - allowed

    print("Allowed:", allowed)
    print("Rejected:", rejected)

    assert allowed == 12
    assert rejected == 8