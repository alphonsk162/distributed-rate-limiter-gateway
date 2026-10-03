from app.rate_limiter.token_bucket import TokenBucketRateLimiter
from app.redis_client import create_redis_client
import sys


client_id = sys.argv[1]

redis_client = create_redis_client()

limiter = TokenBucketRateLimiter(
    redis_client=redis_client,
    capacity=100,
    refill_rate=0,
)

allowed = 0

for _ in range(500):
    if limiter.is_allowed(client_id):
        allowed += 1

print(f"Allowed by this process: {allowed}")