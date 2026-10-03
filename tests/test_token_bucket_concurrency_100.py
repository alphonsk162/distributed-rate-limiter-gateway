from concurrent.futures import ThreadPoolExecutor

from app.rate_limiter.token_bucket import TokenBucketRateLimiter
from app.redis_client import create_redis_client


def test_token_bucket_1000_concurrent_requests():
    redis_client = create_redis_client()

    client_id = "benchmark_concurrency_100"
    key = f"rate_limit:bucket:{client_id}"

    # Start with a completely fresh bucket.
    redis_client.delete(key)

    limiter = TokenBucketRateLimiter(
        redis_client=redis_client,
        capacity=100,
        refill_rate=0,
    )

    def make_request():
        return limiter.is_allowed(client_id)

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(
            executor.map(
                lambda _: make_request(),
                range(1000),
            )
        )

    allowed = sum(results)
    rejected = len(results) - allowed

    print(f"Allowed: {allowed}")
    print(f"Rejected: {rejected}")

    assert allowed == 100
    assert rejected == 900