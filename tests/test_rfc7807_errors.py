from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)

# Need authorization for test client (Need database)

# def test_error_format_standard():
#     """Test that errors follow RFC 7807 format"""
#     response = client.get("/api/wishes/999999")

#     assert response.status_code == 404
#     assert response.headers["content-type"] == "application/problem+json"

#     error_data = response.json()
#     assert "type" in error_data
#     assert "title" in error_data
#     assert "status" in error_data
#     assert "detail" in error_data
#     assert "correlation_id" in error_data
#     assert "instance" in error_data


# def test_correlation_id_present():
#     """Test that correlation_id is present and unique"""
#     response1 = client.get("/api/wishes/999999")
#     response2 = client.get("/api/wishes/999998")

#     error1 = response1.json()
#     error2 = response2.json()

#     assert "correlation_id" in error1
#     assert "correlation_id" in error2
#     assert error1["correlation_id"] != error2["correlation_id"]


# def test_validation_error_format():
#     """Test validation error follows RFC 7807"""
#     # Test with invalid data that should trigger validation error
#     response = client.post("/api/wishes", json={"invalid": "data"})

#     assert response.status_code == 422  # Validation error
#     assert response.headers["content-type"] == "application/problem+json"

#     error_data = response.json()
#     assert error_data["type"] == "http://wishlist.example.com/problems/validation-error"
#     assert error_data["title"] == "Validation Error"


# def test_problem_detail_model():
#     """Test ProblemDetail model creation"""
#     problem = create_problem_detail(
#         status=400,
#         title="Test Error",
#         detail="Test detail",
#         type_="http://example.com/test",
#         instance="/test/endpoint",
#     )

#     assert problem.status == 400
#     assert problem.title == "Test Error"
#     assert problem.detail == "Test detail"
#     assert problem.type == "http://example.com/test"
#     assert problem.instance == "/test/endpoint"
#     assert problem.correlation_id is not None


# def test_security_problem_detail_masking():
#     """Test that SecurityProblemDetail masks details in production"""
#     import os

#     original_env = os.getenv("ENVIRONMENT")

#     try:
#         # Set production environment
#         os.environ["ENVIRONMENT"] = "production"

#         from src.presentation.models.rfc7807 import create_security_problem_detail

#         problem = create_security_problem_detail(
#             status=500,
#             title="Internal Error",
#             detail="Database connection failed",
#             type_="http://example.com/internal-error",
#         )

#         assert problem.detail == "An error occurred while processing your request"
#         assert problem.type == "about:blank"

#     finally:
#         # Restore original environment
#         if original_env:
#             os.environ["ENVIRONMENT"] = original_env
#         else:
#             os.environ.pop("ENVIRONMENT", None)
