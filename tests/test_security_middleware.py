import pytest
from fastapi.testclient import TestClient

from src.app.main import app

# Create separate clients for different test scenarios
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_rate_limiting():
    """Reset rate limiting state before each test"""
    # Since we now use instance variables, each TestClient gets its own middleware instance
    # No need to reset global state
    yield


def test_security_headers():
    """Test that security headers are present in responses"""
    response = client.get("/api/health")

    assert response.status_code == 200
    assert "Strict-Transport-Security" in response.headers
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "X-XSS-Protection" in response.headers
    assert "Referrer-Policy" in response.headers
    assert "Content-Security-Policy" in response.headers


# def test_cors_configuration():
#     """Test CORS configuration"""
#     # Test preflight request
#     response = client.options("/api/health", headers={"Origin": "http://localhost:3000"})

#     assert response.status_code == 200
#     assert "Access-Control-Allow-Origin" in response.headers
#     assert "Access-Control-Allow-Methods" in response.headers
#     assert "Access-Control-Allow-Headers" in response.headers


# def test_cors_allowed_origin():
#     """Test CORS with allowed origin"""
#     # Create fresh client to avoid rate limiting
#     fresh_client = TestClient(app)
#     response = fresh_client.get("/api/health", headers={"Origin": "http://localhost:3000"})

#     assert response.status_code == 200
#     assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
#     assert response.headers["Access-Control-Allow-Credentials"] == "true"


def test_cors_disallowed_origin():
    """Test CORS with disallowed origin"""
    # Create fresh client to avoid rate limiting
    fresh_client = TestClient(app)
    response = fresh_client.get("/api/health", headers={"Origin": "https://malicious.com"})

    assert response.status_code == 200
    # Should not have CORS headers for disallowed origin
    assert "Access-Control-Allow-Origin" not in response.headers


# Need authorization for test client

# def test_security_logging_suspicious_request():
#     """Test that suspicious requests are logged"""
#     # Create fresh client to avoid rate limiting
#     fresh_client = TestClient(app)
#     # Test path traversal attempt
#     response = fresh_client.get("/api/wishes/../../../etc/passwd")
#     # Should not crash, but might return 404 or other error
#     assert response.status_code in [404, 400, 422]


# def test_security_logging_large_request():
#     """Test logging of large requests"""
#     large_data = "x" * 2000000  # 2MB
#     response = client.post("/api/wishes", json={"data": large_data})
#     # Should be handled by request size middleware
#     assert response.status_code in [400, 413, 422]


def test_security_headers_values():
    """Test specific security header values"""
    response = client.get("/api/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
    assert "max-age=31536000" in response.headers["Strict-Transport-Security"]
    assert "includeSubDomains" in response.headers["Strict-Transport-Security"]


def test_csp_header():
    """Test Content Security Policy header"""
    response = client.get("/api/health")

    csp = response.headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "script-src 'self' 'unsafe-inline'" in csp
    assert "style-src 'self' 'unsafe-inline'" in csp
