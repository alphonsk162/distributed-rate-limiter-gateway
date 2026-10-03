from locust import HttpUser, task, between


class RateLimitUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task
    def send_request(self):
        self.client.get(
            "/api/data",
            headers={
                "X-Client-ID": "benchmark-client"
            },
        )