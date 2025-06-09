# from httpx import ASGITransport , AsyncClient 
# from fastapi.testclient import TestClient
# import pytest
# from main import app




# admin_register = "http://127.0.0.1:8000/api/auth/register"

# @pytest.mark.asyncio
# async def test_user_register():
#     async with AsyncClient() as client:
#         user_response = await client.post(url=admin_register , json={
#             "username" : "asasdjasdjs12",
#             "password" : "123456"
#         })

#         assert user_response.status_code == 200


# admin_login = "http://127.0.0.1:8000/api/auth/login"

# @pytest.mark.asyncio
# async def test_user_login():
#     async with AsyncClient() as client:
#         form_data = {
#             "username": "319231100183",
#             "password": "be2005@-Nkt"
#         }
#         response = await client.post(url=admin_login, data=form_data)

#         # Print status and body for debugging
#         print(f"Status: {response.status_code}")
#         print(f"Body: {response.text}")

#         # Assert status code
#         assert response.status_code == 200, f"Expected status code 200, got {response.status_code}: {response.text}"

#         # Parse response as JSON
#         user_data = response.json()
        
#         # Access access_token
#         assert "access_token" in user_data, "Response does not contain access_token"
#         user_token = user_data["access_token"]
        
#         print(f"Access Token: {user_token}")
#         return user_token
    


