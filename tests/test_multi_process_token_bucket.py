import os
import subprocess

from app.redis_client import create_redis_client


def test_token_bucket_across_multiple_processes():
    redis_client = create_redis_client()

    client_id = "multi_process_test"
    key = f"rate_limit:bucket:{client_id}"

    redis_client.delete(key)

    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    process_1 = subprocess.Popen(
        [
            "python",
            "tests/worker_token_bucket.py",
            client_id,
        ],
        stdout=subprocess.PIPE,
        text=True,
        env=env,
    )

    process_2 = subprocess.Popen(
        [
            "python",
            "tests/worker_token_bucket.py",
            client_id,
        ],
        stdout=subprocess.PIPE,
        text=True,
        env=env,
    )

    output_1, _ = process_1.communicate()
    output_2, _ = process_2.communicate()

    print(output_1.strip())
    print(output_2.strip())

    assert "Allowed by this process:" in output_1
    assert "Allowed by this process:" in output_2

    allowed_1 = int(output_1.split(":")[1])
    allowed_2 = int(output_2.split(":")[1])

    assert allowed_1 + allowed_2 == 100