from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)

# async def test_login_ok():
#     resp = await client.post(
#         "/api/auth/login",
#         json = {
#             'email': 'user@test.com',
#             'password': '123456'
#         })
#     assert resp.status_code == 200

# async def test_login_sql_injection():
#     resp = await client.post(
#         "/api/auth/login",
#         json = {
#             'email': 'user@test.com; DROP TABLE users;--',
#             'password': '123456'
#         })
#     assert resp.status_code == 200  # сервер не упал, данные не удалены

# async def test_register_invalid_data():
#     resp = await client.post(
#         "/api/auth/register",
#         json = {
#             'email': '',
#             'password': '123456'
#             })
#     assert resp.status_code in (400, 422)

# async def test_long_string_attack():
#     long_name = "x" * 10000
#     resp = await client.post(
#         "/api/auth/login",
#         json = {
#             'email': f'{long_name}@test.com',
#             'password':'123456'
#         })
#     assert resp.status_code in (400, 422)
