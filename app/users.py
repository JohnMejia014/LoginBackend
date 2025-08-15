from fastapi import APIRouter, Body, Query
from firebase.firebase import firebase_manager

router = APIRouter()

# --- Get User ---
@router.get("/get_user/{user_id}")
def get_user(user_id: str):
    user_info, success, error_message = firebase_manager.get_user(user_id=user_id)
    return {"user_info": user_info, "success": success, "error_message": error_message}


# --- Register User ---
@router.post("/register_user")
def register_user(user_info: dict = Body(...)):
    print('Communicated with API')
    user_info, success, error_message = firebase_manager.register_user(user_info=user_info)
    return {"user_info": user_info, "success": success, "error_message": error_message}


# --- Delete User ---
@router.delete("/delete_user/{user_id}")
def delete_user(user_id: str):
    success, error_message = firebase_manager.delete_user(user_id=user_id)
    return {"success": success, "error_message": error_message}


# --- Update User ---
@router.patch("/update_user/{user_id}")
def update_user(user_id: str, user_updates: dict = Body(...)):
    updated_info, success, error_message = firebase_manager.update_user(user_id=user_id, user_updates=user_updates)
    return {"updated_info": updated_info, "success": success, "error_message": error_message}


# --- Search Users ---
@router.get("/search_user/")
def search_users(name: str = Query(..., min_length=1)):
    # TODO: Will Add this later in any app that sees fit
    return {"results": [f"User matching '{name}'"]}
