from fastapi import Depends 
from httpx import AsyncClient, ASGITransport
import  pytest
from fastapi.testclient import TestClient
from main import app
from src.core.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from test.conftest import db_session


client = TestClient(app)



def override_get_db(db: AsyncSession = Depends(db_session)):
    return db

app.dependency_overrides[get_db] = override_get_db





def test_admin_register():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "bekzod",
            "password": "12345"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "bekzod"


def test_admin_login():
    response = client.post(
        "/api/auth/login",
        data={
            "username": "bekzod",
            "password": "12345"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200



    