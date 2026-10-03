class RuleEngine:
    def __init__(self, rules, default_rule=None, endpoint_rules=None):
        self.rules = rules
        self.default_rule = default_rule
        self.endpoint_rules = endpoint_rules or {}

    def get_rule(self, client_id: str, endpoint=None):
        if client_id in self.rules:
            return self.rules[client_id]

        if endpoint in self.endpoint_rules:
            return self.endpoint_rules[endpoint]

        return self.default_rule