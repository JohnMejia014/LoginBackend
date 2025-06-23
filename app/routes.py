# app/routes.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users():
    return ["Alice", "Bob"]

@router.post("/login")
def login():
    return {"message": "Logged in"}
