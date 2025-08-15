import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- Test Constants ---
UID1 = "test_friend_001"
UID2 = "test_friend_002"

@pytest.fixture(scope="function", autouse=True) 
def setup_users():
    # Register both users
    for uid in [UID1, UID2]:
        client.post("/register_user", json={
            "uid": uid,
            "email": f"{uid}@example.com",
            "full_name": f"Test User {uid[-1]}",
            "username": uid,
            "is_private": True if uid == UID2 else False  # UID2 is private
        })
    yield
    # Pauses then cleans up
    # Clean up
    for uid in [UID1, UID2]:
        client.delete(f"/delete_user/{uid}")


def test_follow_private_user():
    """UID1 tries to follow UID2 who is private — should create a follow request"""
    response = client.post("/request_follow", json={
        "follower_id": UID1,
        "target_user_id": UID2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["error"] == "Follow request sent" # or data['error'] == "Successfully followed"


def test_follow_self_should_fail():
    """User tries to follow themselves"""
    response = client.post("/request_follow", json={
        "follower_id": UID1,
        "target_user_id": UID1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "Cannot follow yourself"


def test_get_pending_follow_requests():
    """Ensure UID2 sees a pending request from UID1"""
    # 1: Send the follow request
    response = client.post("/request_follow", json={
        "follower_id": UID1,
        "target_user_id": UID2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["error"] == "Follow request sent" # or data['error'] == "Successfully followed"

    # 2: Get the follow requests
    response = client.get(f"/get_follow_requests/{UID2}")
    assert response.status_code == 200
    data = response.json()
    assert UID1 in data["follow_requests"]
    assert data["success"] is True


def test_approve_follow_request():
    """UID2 approves UID1's follow request"""
    # 1: Send the follow request
    response = client.post("/request_follow", json={
        "follower_id": UID1,
        "target_user_id": UID2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["error"] == "Follow request sent" # or data['error'] == "Successfully followed"

    # 2: Approve the follow request
    response = client.post("/approve_follow", json={
        "target_user_id": UID2,
        "follower_id": UID1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["error"] == ""


def test_reject_follow_request_should_be_empty_now():
    """Make sure the follow_requests list is now empty after approval"""
    
    # 1: Send the follow request
    response = client.post("/request_follow", json={
        "follower_id": UID1,
        "target_user_id": UID2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["error"] == "Follow request sent" # or data['error'] == "Successfully followed"

    # 2: Approve the follow request
    response = client.post("/approve_follow", json={
        "target_user_id": UID2,
        "follower_id": UID1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["error"] == ""

    # 3: Make sure follow requests is empty
    response = client.get(f"/get_follow_requests/{UID2}")
    assert response.status_code == 200
    data = response.json()
    assert UID1 not in data["follow_requests"]


def test_reject_nonexistent_follow_request():
    """Rejecting a request that was already approved (should still succeed gracefully)"""
    # 1: Send the follow request
    response = client.post("/request_follow", json={
        "follower_id": UID1,
        "target_user_id": UID2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["error"] == "Follow request sent" # or data['error'] == "Successfully followed"

    # 2: Reject the follow request
    response = client.post("/reject_follow", json={
        "target_user_id": UID2,
        "follower_id": UID1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_follow_public_account_auto_success():
    """Set UID2 to public and try follow again - should auto-follow"""
    # Step 1: Set UID2 to public
    response = client.patch(f"/update_user/{UID2}", json={"is_private": False})
    assert response.status_code == 200
    print("Update response:", response.json())

    # Step 2: UID1 follows UID2
    response = client.post("/request_follow", json={
        "follower_id": UID1,
        "target_user_id": UID2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["error"] == "Successfully followed"

    # Step 3: Verify user info was updated
    user1 = get_user(UID1)
    user2 = get_user(UID2)

    assert UID2 in user1["following"]
    assert UID1 in user2["followers"]

def get_user(user_id):
    response = client.get(f"/get_user/{user_id}")
    assert response.status_code == 200
    return response.json()["user_info"]
