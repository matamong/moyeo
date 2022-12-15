from fastapi import APIRouter

from app.api.routes import hello

router = APIRouter()
router.include_router(hello.router, prefix="/hello")