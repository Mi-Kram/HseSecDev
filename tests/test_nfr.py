from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)

# Need authorization for test client (Need database)

# def test_nfr_04_query_validation_price_must_be_number():
#     r = client.get("/api/wishes", params={"price": "abc"})
#     assert r.status_code == 422


# def test_nfr_04_body_validation_rejects_empty_titles_on_create():
#     payload = {
#         "info": {
#             "user_id": 1,
#             "title": "   ",  # will be stripped and fail in service
#             "description": " desc ",
#             "estimate_price": 10,
#         },
#         "notes": [
#             {"title": "Note 1", "description": "d", "received": False},
#         ],
#     }
#     r = client.post("/api/wishes", json=payload)
#     assert r.status_code == 400
#     body = r.json()
#     assert "error" in body


# def test_nfr_01_access_control_foreign_wish_unavailable():
#     r = client.get("/api/wishes/999999")
#     assert r.status_code == 404


# def test_nfr_03_login_attempt_rate_limit():
#     r = None
#     for i in range(6):
#         r = client.post("/api/auth/login", json={'email':'user@test.com','password':"123456"})
#     assert r.status_code == 403


# def test_nfr_08_request_size_limit():
#     r = client.post(
#         url="/api/wishes",
#         json={
#             "info": {
#                 "user_id": 1,
#                 "title": "a" * 1048577,
#                 "description": "desc",
#                 "estimate_price": 10,
#             },
#             "notes": [{"title": "Note 1", "description": "d", "received": False}],
#         },
#     )
#     assert r.status_code == 413
