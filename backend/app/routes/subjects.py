from fastapi import APIRouter, Query, HTTPException
from app.database import get_db

router = APIRouter()

def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/subjects")
async def get_subjects(exam_id: str = Query(...)):
    db = get_db()
    subjects = await db.subjects.find({"exam_id": exam_id}).to_list(100)
    if not subjects:
        raise HTTPException(status_code=404, detail="No subjects found for this exam")
    return [serialize(s) for s in subjects]