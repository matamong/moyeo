from fastapi import APIRouter

from app.api.endpoints import hello, demo, auth, users

api_router = APIRouter()
api_router.include_router(hello.router, prefix="/hello")
api_router.include_router(demo.router, tags=["demo"], prefix="/demo")
api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
api_router.include_router(users.router, tags=["users"], prefix="/users")
