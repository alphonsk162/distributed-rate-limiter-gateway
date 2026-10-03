from app.redis_client import create_redis_client
from app.rules.rule_engine import RuleEngine
from app.rate_limiter.factory import RateLimiterFactory


class RateLimitService:
    def __init__(self, rules, default_rule=None, endpoint_rules=None):
        self.redis = create_redis_client()

        self.rule_engine = RuleEngine(
            rules=rules,
            default_rule=default_rule,
            endpoint_rules=endpoint_rules,
        )

    def is_allowed(self, client_id: str, endpoint=None) -> bool:
        rule = self.rule_engine.get_rule(
            client_id=client_id,
            endpoint=endpoint,
        )

        if rule is None:
            return True
        print(f"Rate limit rule for client '{client_id}': {rule}")
        limiter = RateLimiterFactory.create(
            config=rule,
            redis_client=self.redis,
        )

        return limiter.is_allowed(client_id)