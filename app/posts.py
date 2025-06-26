from fastapi import APIRouter, Body
from firebase.firebase import firebase_manager

router = APIRouter(prefix="/posts", tags=["posts"])

post_example = {
  "post_id": "xyz123",
  "author_id": "abc456",
  "caption": "Beautiful sunset!",
  "image_url": "https://firebase-storage-link.com/photo.jpg",
  "likes": ["uid1", "uid2"],
  "comments": [
    {
      "user_id": "uid3",
      "text": "Wow!",
      "timestamp": "2025-06-24T23:00:00Z"
    }
  ],
  "created_at": "2025-06-24T22:00:00Z"
}

# --- Get Post ---
@router.get("/{post_id}")
def get_post(post_id: str):
    post, success, error_message = firebase_manager.get_post(post_id)
    return {"post": post, "success": success, "error_message": error_message}


# --- Create Post ---
@router.post("/")
def create_post(post_data: dict = Body(...)):
    post, success, error_message = firebase_manager.create_post(post_data)
    return {"post": post, "success": success, "error_message": error_message}


# --- Update Post ---
@router.patch("/{post_id}")
def update_post(post_id: str, updates: dict = Body(...)):
    updated_post, success, error_message = firebase_manager.update_post(post_id, updates)
    return {"post": updated_post, "success": success, "error_message": error_message}


# --- Delete Post ---
@router.delete("/{post_id}")
def delete_post(post_id: str):
    success, error_message = firebase_manager.delete_post(post_id)
    return {"success": success, "error_message": error_message}


# --- Get All Posts (Feed) ---
@router.get("/feed")
def get_feed():
    posts, success, error_message = firebase_manager.get_all_posts()
    return {"posts": posts, "success": success, "error_message": error_message}


# --- Like a Post ---
@router.post("/{post_id}/like")
def like_post(post_id: str, user_id: str = Body(...)):
    success, error_message = firebase_manager.like_post(post_id, user_id)
    return {"success": success, "error_message": error_message}


# --- Comment on a Post ---
@router.post("/{post_id}/comment")
def comment_post(post_id: str, comment_data: dict = Body(...)):
    success, error_message = firebase_manager.comment_post(post_id, comment_data)
    return {"success": success, "error_message": error_message}


# --- Share a Post ---
@router.post("/{post_id}/share")
def share_post(post_id: str, user_id: str = Body(...)):
    success, error_message = firebase_manager.share_post(post_id, user_id)
    return {"success": success, "error_message": error_message}
