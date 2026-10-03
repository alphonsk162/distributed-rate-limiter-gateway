from app.rate_limiter.base import RateLimiter
from app.rate_limiter.factory import RateLimiterFactory
from app.rate_limiter.fixed_window import FixedWindowRateLimiter
from app.rate_limiter.token_bucket import TokenBucketRateLimiter


# def test_factory_creates_fixed_window():
#     config = {
#         "algorithm": "fixed_window",
#         "limit": 5,
#         "window_seconds": 10,
#     }

#     limiter = RateLimiterFactory.create(config)

#     assert isinstance(limiter, FixedWindowRateLimiter)
#     assert isinstance(limiter, RateLimiter)


# def test_factory_creates_token_bucket():
#     config = {
#         "algorithm": "token_bucket",
#         "capacity": 10,
#         "refill_rate": 2,
#     }

#     limiter = RateLimiterFactory.create(config)

#     assert isinstance(limiter, TokenBucketRateLimiter)
#     assert isinstance(limiter, RateLimiter)


# def test_factory_rejects_unknown_algorithm():
#     config = {
#         "algorithm": "something_invalid",
#     }

#     try:
#         RateLimiterFactory.create(config)
#         assert False
#     except ValueError:
#         pass