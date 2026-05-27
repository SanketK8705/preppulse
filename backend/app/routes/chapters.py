from fastapi import APIRouter, Query, HTTPException
from app.database import get_db

router = APIRouter()

def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/chapters")
async def get_chapters(subject_id: str = Query(...)):
    db = get_db()
    chapters = await db.chapters.find({"subject_id": subject_id}).to_list(100)
    if not chapters:
        raise HTTPException(status_code=404, detail="No chapters found for this subject")
    return [serialize(c) for c in chapters]