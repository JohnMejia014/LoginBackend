from fastapi import FastAPI
from app.friends import router as friend_router
from app.users import router as user_router
from app.posts import router as post_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(post_router, prefix="/posts", tags=["posts"])
app.include_router(friend_router)