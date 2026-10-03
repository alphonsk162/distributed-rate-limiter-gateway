import redis


def create_redis_client():
    return redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
    )