from fastapi.testclient import TestClient

from src.app.main import app

# Create separate clients for different test scenarios
client = TestClient(app)

# Need authorization for test client (Need database)

# def test_complete_security_flow():
#     """Test complete security flow with all middleware and validation"""
#     # Create fresh client to avoid rate limiting
#     fresh_client = TestClient(app)

#     # Test normal request
#     response = fresh_client.get("/api/health")
#     assert response.status_code == 200

#     # Check security headers
#     assert "Strict-Transport-Security" in response.headers
#     assert "X-Content-Type-Options" in response.headers

#     # Test error handling with RFC 7807
#     response = fresh_client.get("/api/wishes/999999")
#     assert response.status_code == 404
#     assert response.headers["content-type"] == "application/problem+json"

#     error_data = response.json()
#     assert "correlation_id" in error_data
#     assert "type" in error_data
#     assert "title" in error_data


# def test_validation_with_security_headers():
#     """Test that validation errors include security headers"""
#     # Create fresh client to avoid rate limiting
#     fresh_client = TestClient(app)

#     # Test with invalid data
#     response = fresh_client.post("/api/wishes", json={"invalid": "data"})

#     # Should have validation error
#     assert response.status_code in [400, 422]

#     # Should have security headers
#     assert "X-Content-Type-Options" in response.headers
#     assert "X-Frame-Options" in response.headers

#     # Should have RFC 7807 format if 400
#     if response.status_code == 400:
#         assert response.headers["content-type"] == "application/problem+json"


# def test_rate_limiting_with_security_headers():
#     """Test that rate limited responses include security headers"""
#     # Make many requests to trigger rate limiting
#     for i in range(101):
#         response = client.get("/api/health")
#         if response.status_code == 429:
#             break

#     assert response.status_code == 429

#     # Should have security headers even when rate limited
#     assert "X-Content-Type-Options" in response.headers
#     assert "X-Frame-Options" in response.headers

#     # Should have RFC 7807 format
#     assert response.headers["content-type"] == "application/problem+json"


# def test_cors_with_security_headers():
#     """Test that CORS responses include security headers"""
#     # Create fresh client to avoid rate limiting
#     fresh_client = TestClient(app)

#     response = fresh_client.get("/api/health", headers={"Origin": "http://localhost:3000"})

#     assert response.status_code == 200

#     # Should have CORS headers
#     assert "Access-Control-Allow-Origin" in response.headers

#     # Should also have security headers
#     assert "X-Content-Type-Options" in response.headers
#     assert "X-Frame-Options" in response.headers


# def test_error_correlation_across_requests():
#     """Test that correlation IDs are unique across different requests"""
#     # Create fresh client to avoid rate limiting
#     fresh_client = TestClient(app)

#     response1 = fresh_client.get("/api/wishes/999999")
#     response2 = fresh_client.get("/api/wishes/999998")

#     if response1.status_code == 404 and response2.status_code == 404:
#         error1 = response1.json()
#         error2 = response2.json()

#         assert error1["correlation_id"] != error2["correlation_id"]
#         assert "correlation_id" in error1
#         assert "correlation_id" in error2


# def test_security_middleware_order():
#     """Test that middleware is applied in correct order"""
#     # Create fresh client to avoid rate limiting
#     fresh_client = TestClient(app)

#     response = fresh_client.get("/health")

#     # Should have all security headers
#     security_headers = [
#         "Strict-Transport-Security",
#         "X-Content-Type-Options",
#         "X-Frame-Options",
#         "X-XSS-Protection",
#         "Referrer-Policy",
#         "Content-Security-Policy",
#     ]

#     for header in security_headers:
#         assert header in response.headers, f"Missing security header: {header}"


# def test_large_request_handling():
#     """Test handling of large requests with all middleware"""
#     # Create fresh client to avoid rate limiting
#     fresh_client = TestClient(app)

#     # Test with request that's too large
#     large_data = "x" * 2000000  # 2MB

#     response = fresh_client.post("/api/wishes", json={"data": large_data})

#     # Should be rejected by request size middleware
#     assert response.status_code in [400, 413, 422]

#     # For 413 responses, security headers might not be added by RequestSizeLimitMiddleware
#     # So we'll just check that the request was properly rejected
#     if response.status_code == 413:
#         assert response.headers["content-type"] == "text/plain; charset=utf-8"
#     else:
#         # Should still have security headers for other error types
#         assert "X-Content-Type-Options" in response.headers
#         assert "X-Frame-Options" in response.headers
