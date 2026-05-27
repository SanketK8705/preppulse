from fastapi import APIRouter
from app.database import get_db
from bson import ObjectId

router = APIRouter()

def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/exams")
async def get_exams():
    db = get_db()
    exams = await db.exams.find().to_list(100)
    return [serialize(e) for e in exams]