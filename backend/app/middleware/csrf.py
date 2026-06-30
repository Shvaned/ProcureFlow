import secrets

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.exceptions import AuthorizationException

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
EXEMPT_PATHS = {"/api/v1/auth/login", "/api/v1/auth/refresh"}


class CSRFMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, cookie_name: str = "csrf_token", header_name: str = "X-CSRF-Token"):
        super().__init__(app)
        self.cookie_name = cookie_name
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next) -> Response:
        # Exempt auth endpoints from CSRF
        if request.url.path in EXEMPT_PATHS:
            response = await call_next(request)
            if self.cookie_name not in request.cookies:
                response.set_cookie(
                    key=self.cookie_name,
                    value=secrets.token_urlsafe(32),
                    httponly=False,
                    samesite="strict",
                    secure=False,
                )
            return response

        if request.method.upper() in SAFE_METHODS:
            response = await call_next(request)
            if self.cookie_name not in request.cookies:
                response.set_cookie(
                    key=self.cookie_name,
                    value=secrets.token_urlsafe(32),
                    httponly=False,
                    samesite="strict",
                    secure=False,
                )
            return response

        csrf_cookie = request.cookies.get(self.cookie_name)
        csrf_header = request.headers.get(self.header_name)

        if not csrf_cookie or not csrf_header or csrf_cookie != csrf_header:
            raise AuthorizationException("CSRF token validation failed")

        response = await call_next(request)
        return response
