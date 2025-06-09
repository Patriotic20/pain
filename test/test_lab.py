from fastapi import Depends
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


# USER_DATA = 


def test_admin_register():
    response = client.post(
        url = "/api/auth/register",
        json={
        "username": "bekzod",
        "password": "12345",
        }
    )

    print(response.json())
    assert response.status_code == 200
    assert response.json()["username"] == "bekzod"