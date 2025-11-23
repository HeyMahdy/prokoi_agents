from typing import Callable, Awaitable
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

import pprint
class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Public routes (skip authentication)
        public_paths = {
            "/docs",
            "/redoc",
            "/openapi.json"
        }

        if path in public_paths:
            return await call_next(request)

        # Normal auth logic for other routes
        auth_header = request.headers.get("authorization", "")

        if not auth_header.lower().startswith("bearer "):
            return JSONResponse({"detail": "Not authenticated"}, status_code=401)

        token = auth_header.split(" ", 1)[1].strip()

        print("getting the token")
        print(token)

        request.scope.setdefault("state", {})
        request.scope["state"]["token"] = token

        return await call_next(request)
