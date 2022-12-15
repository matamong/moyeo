from fastapi import APIRouter

router = APIRouter()

@router.get("", name="hello:test-api")
async def get_hello() -> str:
    return "Hello World!"