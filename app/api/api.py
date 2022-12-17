from fastapi import APIRouter

from app.api.endpoints import hello
from app.api.endpoints import demo

router = APIRouter()
router.include_router(hello.router, prefix="/hello")
router.include_router(demo.router, tags=["demo"], prefix="/demo")