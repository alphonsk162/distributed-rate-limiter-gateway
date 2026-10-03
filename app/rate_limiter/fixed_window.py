import time

from .base import RateLimiter


class FixedWindowRateLimiter(RateLimiter):

    def __init__(
        self,
        redis_client,
        limit: int,
        window_seconds: int,
    ):
        self.redis = redis_client
        self.limit = limit
        self.window_seconds = window_seconds

    def is_allowed(self, client_id: str) -> bool:
        current_window = int(time.time()) // self.window_seconds

        key = f"rate_limit:fixed:{client_id}:{current_window}"

        script = """
        local count = redis.call("INCR", KEYS[1])

        if count == 1 then
            redis.call("EXPIRE", KEYS[1], ARGV[1])
        end

        return count
        """

        count = self.redis.eval(
            script,
            1,
            key,
            self.window_seconds,
        )

        return count <= self.limit