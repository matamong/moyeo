from fastapi import APIRouter

from app.api.endpoints import hello, demo

api_router = APIRouter()
api_router.include_router(hello.router, prefix="/hello")
api_router.include_router(demo.router, tags=["demo"], prefix="/demo")