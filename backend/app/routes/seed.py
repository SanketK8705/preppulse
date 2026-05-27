from fastapi import APIRouter
from app.services.seed_service import seed_all

router = APIRouter()

@router.post("/seed")
async def trigger_seed():
    await seed_all()
    return {"status": "ok", "message": "Database seeded successfully"}