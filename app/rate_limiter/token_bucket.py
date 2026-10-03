import time, json

from .base import RateLimiter


class TokenBucketRateLimiter(RateLimiter):

    def __init__(
        self,
        redis_client,
        capacity: int,
        refill_rate: float,
    ):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.redis = redis_client

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        key = f"rate_limit:bucket:{client_id}"
        script = """
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])
        local bucket_data = redis.call("GET", KEYS[1])
        if not bucket_data then
            local bucket = {tokens = capacity - 1, last_refill = now}
            redis.call("SET", KEYS[1], cjson.encode(bucket))
            return 1
            end
        local bucket = cjson.decode(bucket_data)
        local elapsed = now - bucket.last_refill
        local tokens_to_add = elapsed * refill_rate
        bucket.tokens = math.min(capacity, bucket.tokens + tokens_to_add)
        bucket.last_refill = now
        if bucket.tokens < 1 then
            redis.call("SET", KEYS[1], cjson.encode(bucket))
            return 0
            end
        bucket.tokens = bucket.tokens - 1
        redis.call("SET", KEYS[1], cjson.encode(bucket))
        return 1
        """
        result = self.redis.eval(
        script, 1, key, self.capacity, self.refill_rate, now
        )
        return bool(result)