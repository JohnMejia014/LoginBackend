from fastapi import APIRouter, Body
from firebase.firebase import firebase_manager

router = APIRouter()


@router.post("/request_follow")
def request_follow(data: dict = Body(...)):
    success, error = firebase_manager.request_follow(data["follower_id"], data["target_user_id"])
    return {'success': success, 'error': error}

@router.post("/approve_follow")
def approve_follow(data: dict = Body(...)):
    success, error = firebase_manager.approve_follow_request(data["target_user_id"], data["follower_id"])
    return {'success': success, 'error': error}

@router.post("/reject_follow")
def reject_follow(data: dict = Body(...)):
    success, error = firebase_manager.reject_follow_request(data["target_user_id"], data["follower_id"])
    return {'success': success, 'error': error}

@router.get("/get_follow_requests/{user_id}")
def get_requests(user_id: str):
    follow_requests, success, error = firebase_manager.get_pending_follow_requests(user_id)
    return {'follow_requests': follow_requests, 'success': success, 'error': error}