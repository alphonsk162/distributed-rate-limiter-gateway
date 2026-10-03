CLIENT_RULES = {
    "api_test_client": {
        "algorithm": "token_bucket",
        "capacity": 5,
        "refill_rate": 1,
    },

    "benchmark-client": {
        "algorithm": "token_bucket",
        "capacity": 100000,
        "refill_rate": 100000,
    },
}