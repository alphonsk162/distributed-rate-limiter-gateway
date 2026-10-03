from app.rules.rule_engine import RuleEngine


def test_rule_engine_returns_rule_for_client():
    rules = {
        "alice": {
            "algorithm": "fixed_window",
            "limit": 10,
            "window_seconds": 60,
        }
    }

    engine = RuleEngine(rules)

    rule = engine.get_rule("alice")

    assert rule == {
        "algorithm": "fixed_window",
        "limit": 10,
        "window_seconds": 60,
    }


def test_rule_engine_returns_default_rule():
    rules = {
        "alice": {
            "algorithm": "fixed_window",
            "limit": 10,
            "window_seconds": 60,
        }
    }

    default_rule = {
        "algorithm": "token_bucket",
        "capacity": 20,
        "refill_rate": 2,
    }

    engine = RuleEngine(rules, default_rule=default_rule)

    rule = engine.get_rule("bob")

    assert rule == default_rule

def test_rule_engine_returns_endpoint_rule():
    rules = {
        "alice": {
            "algorithm": "fixed_window",
            "limit": 10,
            "window_seconds": 60,
        }
    }

    endpoint_rules = {
        "/api/orders": {
            "algorithm": "fixed_window",
            "limit": 5,
            "window_seconds": 60,
        }
    }

    engine = RuleEngine(
        rules=rules,
        endpoint_rules=endpoint_rules,
    )

    rule = engine.get_rule(
        client_id="bob",
        endpoint="/api/orders",
    )

    assert rule == {
        "algorithm": "fixed_window",
        "limit": 5,
        "window_seconds": 60,
    }