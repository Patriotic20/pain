import  pytest
from fastapi.testclient import TestClient
from main import app
from src.core.base import get_db


client = TestClient(app)

@pytest.fixture
def override_get_db(db_session):
    return db_session

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