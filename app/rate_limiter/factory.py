from .fixed_window import FixedWindowRateLimiter
from .token_bucket import TokenBucketRateLimiter


class RateLimiterFactory:

    @staticmethod
    def create(redis_client, config):
        algorithm = config["algorithm"]

        if algorithm == "fixed_window":
            return FixedWindowRateLimiter(
                redis_client=redis_client,
                limit=config["limit"],
                window_seconds=config["window_seconds"],
            )

        if algorithm == "token_bucket":
            return TokenBucketRateLimiter(
                redis_client=redis_client,
                capacity=config["capacity"],
                refill_rate=config["refill_rate"],
            )

        raise ValueError(
            f"Unsupported rate limiter algorithm: {algorithm}"
        )