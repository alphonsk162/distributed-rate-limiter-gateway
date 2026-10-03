# Rate Limiter + API Gateway

A distributed rate-limiting API gateway built with **Python, FastAPI, Redis, and Lua**.

The gateway supports multiple rate-limiting algorithms and uses Redis as shared state so that rate limits remain consistent across multiple application workers.

## Features

* Fixed Window rate limiting
* Token Bucket rate limiting
* Redis-backed shared state
* Atomic rate-limit operations using Redis Lua scripts
* Configurable client-specific and default policies
* Concurrent request handling
* FastAPI HTTP API
* Multi-worker support

## Architecture

```text
Client
  ↓
FastAPI Gateway
  ↓
RateLimitService
  ↓
RuleEngine
  ↓
RateLimiterFactory
  ↓
Token Bucket / Fixed Window
  ↓
Redis + Lua
```

### Main Components

* **Rule Engine** — selects the rate-limit policy for a client.
* **Factory** — creates the appropriate rate-limiter implementation.
* **Token Bucket / Fixed Window** — implements the rate-limiting algorithms.
* **Redis** — stores shared rate-limit state.
* **Lua** — performs multi-step Redis operations atomically.
* **FastAPI** — exposes the rate limiter through an HTTP API.

## Example

A Token Bucket policy can be configured as:

```python
{
    "algorithm": "token_bucket",
    "capacity": 10,
    "refill_rate": 2
}
```

This allows an initial burst of 10 requests and then replenishes the bucket at 2 tokens per second.

When the limit is exceeded, the API returns:

```text
HTTP 429 Too Many Requests
```

## Running Locally

### 1. Start Redis

```bash
brew services start redis
```

Verify:

```bash
redis-cli ping
```

Expected:

```text
PONG
```

### 2. Activate the virtual environment

```bash
source venv/bin/activate
```

### 3. Start the API

```bash
uvicorn app.main:app --workers 3
```

The API is available at:

```text
http://127.0.0.1:8000
```

### 4. Send a request

```bash
curl -i \
  -H "X-Client-ID: my-client" \
  http://127.0.0.1:8000/api/data
```

The gateway returns `200` when the request is allowed and `429` when the rate limit is exceeded.

## Testing

Run the complete test suite:

```bash
pytest
```

Concurrency testing demonstrated that:

```text
1,000 concurrent requests
→ 100 allowed
→ 900 rejected
```

Two independent processes sharing the same Redis bucket also maintained the same global limit.

## Benchmark

Using Locust with 50 concurrent users for 20 seconds:

| Configuration |   Throughput | p95 Latency | Failures |
| ------------- | -----------: | ----------: | -------: |
| 1 worker      |   ~993 req/s |       30 ms |       0% |
| 3 workers     | ~1,024 req/s |       22 ms |       0% |

Results were measured locally on a MacBook with Redis running locally, so they represent local benchmark results rather than production capacity.

## Tech Stack

* Python
* FastAPI
* Redis
* Redis Lua
* Locust
* Pytest
* Uvicorn
