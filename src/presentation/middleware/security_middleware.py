import logging
import time
from collections import defaultdict, deque
from typing import List

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Security headers
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        if request.url.path.startswith("/docs"):
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' https://fastapi.tiangolo.com; "
                "font-src 'self' https://cdn.jsdelivr.net;"
            )
        else:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'"
            )

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting requests"""

    def __init__(self, app, requests_per_minute: int = 100, burst_limit: int = 20):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        # Use instance variables instead of class variables
        self._requests = defaultdict(lambda: deque())
        self._blocked_ips = set()

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Clean old requests (older than 1 minute)
        if client_ip in self._requests:
            while self._requests[client_ip] and current_time - self._requests[client_ip][0] > 60:
                self._requests[client_ip].popleft()

        # Check rate limit
        if len(self._requests[client_ip]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "type": "https://wishlist.example.com/problems/rate-limit-exceeded",
                    "title": "Rate Limit Exceeded",
                    "status": 429,
                    "detail": "Too many requests. Please try again later.",
                    "correlation_id": str(int(current_time)),
                },
                headers={"Content-Type": "application/problem+json"},
            )

        # Check burst limit
        recent_requests = [
            req_time for req_time in self._requests[client_ip] if current_time - req_time < 10
        ]
        if len(recent_requests) >= self.burst_limit:
            logger.warning(f"Burst limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "type": "https://wishlist.example.com/problems/burst-limit-exceeded",
                    "title": "Burst Limit Exceeded",
                    "status": 429,
                    "detail": "Too many requests in short time. Please slow down.",
                    "correlation_id": str(int(current_time)),
                },
                headers={"Content-Type": "application/problem+json"},
            )

        # Record this request
        self._requests[client_ip].append(current_time)

        response = await call_next(request)
        return response


class SecurityLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for security event logging"""

    async def dispatch(self, request: Request, call_next):
        # start_time = time.time()
        # user_agent = request.headers.get("user-agent", "unknown")
        client_ip = request.client.host if request.client else "unknown"

        # Log suspicious patterns
        if self._is_suspicious_request(request):
            logger.warning(f"Suspicious request from {client_ip}: {request.method} {request.url}")

        response = await call_next(request)

        # Log security events
        if response.status_code >= 400:
            logger.warning(
                f"Error response {response.status_code} "
                f"for {request.method} {request.url} from {client_ip}"
            )

        # Log large requests
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 1000000:  # 1MB
            logger.info(f"Large request ({content_length} bytes) from {client_ip}")

        return response

    def _is_suspicious_request(self, request: Request) -> bool:
        """Check for suspicious request patterns"""
        suspicious_patterns = [
            "..",  # Path traversal
            "<script",  # XSS attempt
            "union select",  # SQL injection
            "javascript:",  # XSS attempt
            "eval(",  # Code injection
        ]

        url_str = str(request.url).lower()
        for pattern in suspicious_patterns:
            if pattern in url_str:
                return True

        return False


class CORSMiddleware(BaseHTTPMiddleware):
    """Custom CORS middleware with security restrictions"""

    def __init__(self, app, allowed_origins: List[str] = None):
        super().__init__(app)
        self.allowed_origins = allowed_origins or [
            "http://localhost:3000",
            "https://wishlist.example.com",
        ]
        self.allowed_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allowed_headers = ["Content-Type", "Authorization", "X-Requested-With"]

    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")

        # Handle preflight requests
        if request.method == "OPTIONS":
            response = Response()
            if origin in self.allowed_origins:
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allowed_methods)
                response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allowed_headers)
                response.headers["Access-Control-Max-Age"] = "86400"
            return response

        response = await call_next(request)

        # Add CORS headers for allowed origins
        if origin in self.allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"

        return response
