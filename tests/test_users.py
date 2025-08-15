import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Shared user ID for test consistency
TEST_USER_ID = "test_user_123"

def test_register_user():
    user_info = {
        "uid": TEST_USER_ID,
        "email": "test@example.com",
        "full_name": "Test User",
        "provider": "google"
    }
    response = client.post("/register_user", json=user_info)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "email" in data["user_info"]

def test_get_user():
    time.sleep(1)
    response = client.get(f"/get_user/{TEST_USER_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["user_info"]["email"] == "test@example.com"

def test_update_user():
    time.sleep(2)
    updates = {
        "user_id": TEST_USER_ID,
        "bio": "Updated test bio",
        "is_online": False
    }
    response = client.patch("/update_user", json=updates)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["updated_info"]["bio"] == "Updated test bio"
    assert data["updated_info"]["is_online"] is False

def test_search_user():
    response = client.get("/search_user/", params={"name": "Test"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert any("Test" in result for result in data["results"])

def test_delete_user():
    time.sleep(3)  # (optional) give Firestore a small buffer before delete
    response = client.delete(f"/delete_user/{TEST_USER_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
