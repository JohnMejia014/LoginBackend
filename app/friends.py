from fastapi import APIRouter, Body
from firebase.firebase import firebase_manager

router = APIRouter(prefix="/friends", tags=["friends"])


# --- Send Friend Request ---
@router.post("/request")
def send_friend_request(data: dict = Body(...)):
    """
    Send a friend request from one user to another
    data = {"from_user": "uid1", "to_user": "uid2"}
    """
    success, error_message = firebase_manager.send_friend_request(data["from_user"], data["to_user"])
    return {"success": success, "error_message": error_message}


# --- Accept Friend Request ---
@router.post("/accept")
def accept_friend_request(data: dict = Body(...)):
    """
    Accept a friend request
    """
    success, error_message = firebase_manager.accept_friend_request(data["from_user"], data["to_user"])
    return {"success": success, "error_message": error_message}


# --- Decline Friend Request ---
@router.post("/decline")
def decline_friend_request(data: dict = Body(...)):
    """
    Decline a friend request
    """
    success, error_message = firebase_manager.decline_friend_request(data["from_user"], data["to_user"])
    return {"success": success, "error_message": error_message}


# --- Remove Friend ---
@router.post("/remove")
def remove_friend(data: dict = Body(...)):
    """
    Remove a friend connection
    """
    success, error_message = firebase_manager.remove_friend(data["user_id"], data["friend_id"])
    return {"success": success, "error_message": error_message}


# --- Get Friends List ---
@router.get("/{user_id}/list")
def get_friends_list(user_id: str):
    friends, success, error_message = firebase_manager.get_friends_list(user_id)
    return {"friends": friends, "success": success, "error_message": error_message}


# --- Get Pending Requests ---
@router.get("/{user_id}/pending")
def get_pending_requests(user_id: str):
    pending, success, error_message = firebase_manager.get_pending_requests(user_id)
    return {"pending_requests": pending, "success": success, "error_message": error_message}
