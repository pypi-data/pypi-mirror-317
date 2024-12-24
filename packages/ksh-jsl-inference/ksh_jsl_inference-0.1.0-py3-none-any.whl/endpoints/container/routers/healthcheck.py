from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def readiness_probe():
    return "Ready"
