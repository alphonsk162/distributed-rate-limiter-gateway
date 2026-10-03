from fastapi import FastAPI, Header, HTTPException

from app.gateway.rate_limit_service import RateLimitService
import os
from app.config.rate_limits import CLIENT_RULES
app = FastAPI()




rate_limit_service = RateLimitService(
    rules=CLIENT_RULES,
    default_rule={}
)


@app.get("/api/data")
def get_data(x_client_id: str = Header(...)):
    allowed = rate_limit_service.is_allowed(
        client_id=x_client_id,
        endpoint="/api/data",
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "message": "Rate limit exceeded",
                "worker_pid": os.getpid(),
            },
        )

    return {
        "message": "Request successful",
        "worker_pid": os.getpid(),
    }


