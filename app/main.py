from fastapi import FastAPI

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.api.audit import router
from app.core.limiter import limiter
from app.middleware.request_id import RequestIDMiddleware


app = FastAPI(title="Page Pulse API")

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(RequestIDMiddleware)

app.include_router(router)