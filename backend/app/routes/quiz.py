from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
from app.database import get_db
from app.models.models import StartQuizRequest, AnswerRequest

router = APIRouter()


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc


def fmt_question(q, index, total):
    return {
        "id": str(q["_id"]),
        "text": q["text"],
        "options": q["options"],
        "difficulty": q["difficulty"],
        "question_number": index + 1,
        "total_questions": total,
    }


@router.post("/quiz/start")
async def start_quiz(req: StartQuizRequest):
    db = get_db()

    # Upsert user
    user = await db.users.find_one_and_update(
        {"device_id": req.device_id},
        {"$set": {"last_active": datetime.utcnow(), "nickname": req.nickname},
         "$setOnInsert": {"created_at": datetime.utcnow(), "device_id": req.device_id}},
        upsert=True,
        return_document=True,
    )
    user_id = str(user["_id"])

    # Validate chapter
    if not ObjectId.is_valid(req.chapter_id):
        raise HTTPException(status_code=400, detail="Invalid chapter_id")
    chapter = await db.chapters.find_one({"_id": ObjectId(req.chapter_id)})
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Get questions for chapter
    questions = await db.questions.find({"chapter_id": req.chapter_id}).to_list(100)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions in this chapter")

    question_ids = [str(q["_id"]) for q in questions]

    # Create session
    session_doc = {
        "user_id": user_id,
        "chapter_id": req.chapter_id,
        "question_ids": question_ids,
        "current_index": 0,
        "score": 0,
        "status": "active",
        "started_at": datetime.utcnow(),
        "completed_at": None,
    }
    s_res = await db.quiz_sessions.insert_one(session_doc)
    session_id = str(s_res.inserted_id)

    first_q = questions[0]
    return {
        "session_id": session_id,
        "question": fmt_question(first_q, 0, len(questions)),
        "chapter_name": chapter["name"],
    }


@router.post("/quiz/answer")
async def submit_answer(req: AnswerRequest):
    db = get_db()

    if not ObjectId.is_valid(req.session_id):
        raise HTTPException(status_code=400, detail="Invalid session_id")

    session = await db.quiz_sessions.find_one({"_id": ObjectId(req.session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session["status"] != "active":
        raise HTTPException(status_code=400, detail="Session already completed")

    # Get question
    if not ObjectId.is_valid(req.question_id):
        raise HTTPException(status_code=400, detail="Invalid question_id")
    question = await db.questions.find_one({"_id": ObjectId(req.question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = req.selected_index == question["correct_index"]

    # Parse shown_at
    try:
        shown_at = datetime.fromisoformat(req.shown_at.replace("Z", "+00:00"))
    except Exception:
        shown_at = datetime.utcnow()

    from datetime import timezone
    answered_at = datetime.now(timezone.utc)
    duration_ms = int((answered_at - shown_at).total_seconds() * 1000)
    if duration_ms < 0:
        duration_ms = 0

    # Save response
    await db.quiz_responses.insert_one({
        "session_id": req.session_id,
        "question_id": req.question_id,
        "selected_index": req.selected_index,
        "is_correct": is_correct,
        "shown_at": shown_at,
        "answered_at": answered_at,
        "response_duration_ms": duration_ms,
    })

    # Advance session
    current_index = session["current_index"] + 1
    question_ids = session["question_ids"]
    total = len(question_ids)
    score_delta = 1 if is_correct else 0
    new_score = session["score"] + score_delta

    # Check if done
    if current_index >= total:
        await db.quiz_sessions.update_one(
            {"_id": ObjectId(req.session_id)},
            {"$set": {
                "current_index": current_index,
                "score": new_score,
                "status": "completed",
                "completed_at": datetime.utcnow(),
            }}
        )
        return {
            "is_correct": is_correct,
            "correct_index": question["correct_index"],
            "explanation": question["explanation"],
            "is_last": True,
            "next_question": None,
            "session_id": req.session_id,
        }

    # Get next question
    next_q_id = question_ids[current_index]
    next_q = await db.questions.find_one({"_id": ObjectId(next_q_id)})

    await db.quiz_sessions.update_one(
        {"_id": ObjectId(req.session_id)},
        {"$set": {"current_index": current_index, "score": new_score}}
    )

    return {
        "is_correct": is_correct,
        "correct_index": question["correct_index"],
        "explanation": question["explanation"],
        "is_last": False,
        "next_question": fmt_question(next_q, current_index, total),
        "session_id": req.session_id,
    }


@router.get("/quiz/{session_id}/result")
async def get_result(session_id: str):
    db = get_db()

    if not ObjectId.is_valid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session_id")

    session = await db.quiz_sessions.find_one({"_id": ObjectId(session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get all responses for this session
    responses = await db.quiz_responses.find(
        {"session_id": session_id}
    ).to_list(100)

    # Get questions with correct answers
    question_ids = [ObjectId(qid) for qid in session["question_ids"]]
    questions = await db.questions.find(
        {"_id": {"$in": question_ids}}
    ).to_list(100)
    q_map = {str(q["_id"]): q for q in questions}

    # Build per-question result
    q_results = []
    for resp in responses:
        q = q_map.get(resp["question_id"], {})
        q_results.append({
            "question_text": q.get("text", ""),
            "options": q.get("options", []),
            "correct_index": q.get("correct_index", 0),
            "selected_index": resp["selected_index"],
            "is_correct": resp["is_correct"],
            "explanation": q.get("explanation", ""),
            "response_duration_ms": resp.get("response_duration_ms", 0),
        })

    total = len(session["question_ids"])
    score = session["score"]

    return {
        "session_id": session_id,
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 1) if total else 0,
        "status": session["status"],
        "started_at": session["started_at"].isoformat(),
        "completed_at": session.get("completed_at", "").isoformat() if session.get("completed_at") else None,
        "questions": q_results,
    }