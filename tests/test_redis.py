from app.redis_client import create_redis_client


def test_redis_connection():
    redis_client = create_redis_client()

    assert redis_client.ping() is True